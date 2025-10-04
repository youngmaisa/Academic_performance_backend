from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
import os
import joblib
import numpy as np
import pandas as pd
from models.class_model import Class
from models.realgrade_model import RealGrade
from models.formresponsebackup import FormResponseBackup
from services.predictor_loader import load_model, load_columns, load_encoder
from models.predictrisk_model import PredictedRisk
from models.user_model import User
import lime
import lime.lime_tabular
import json
from models.limeexplanation_model import LIMEExplanation
BASE_PATH = "ml_models"


def predict_by_stage(stage: int, class_id: int, db: Session) -> List[dict]:
    if stage not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Stage inválido. Debe ser 1, 2 o 3.")

    # 1. Recuperar respuestas
    backups = db.query(FormResponseBackup).filter(
        FormResponseBackup.class_id == class_id,
        FormResponseBackup.prediction_stage == stage
    ).all()

    if not backups:
        raise HTTPException(status_code=404, detail="No hay respuestas para generar esta predicción")

    # 2. Notas si stage >= 2
    grades_map = {}
    if stage >= 2:
        real_grades = db.query(RealGrade).filter(RealGrade.class_id == class_id).all()
        grades_map = {g.student_id: g for g in real_grades}

    data, student_ids = [], []
    for b in backups:
        student_ids.append(b.student_id)
        class_ = db.query(Class).filter(Class.id == class_id).first()
        subject = class_.subject if class_ else "mat"

        entry = {
            "subject": subject,
            "sex": b.answer_1,
            "age": int(b.answer_2),
            "address": b.answer_3,
            "guardian": b.answer_4,
            "traveltime": int(b.answer_5),
            "studytime": int(b.answer_6),
            "failures": int(b.answer_7),
            "schoolsup": b.answer_8,
            "famsup": b.answer_9,
            "paid": b.answer_10,
            "activities": b.answer_11,
            "higher": b.answer_12,
            "internet": b.answer_13,
            "romantic": b.answer_14,
            "famrel": int(b.answer_15),
            "freetime": int(b.answer_16),
            "goout": int(b.answer_17),
            "Dalc": int(b.answer_18),
            "Walc": int(b.answer_19),
            "health": int(b.answer_20)
        }

        grades = grades_map.get(b.student_id)
        if stage >= 2:
            if not grades or grades.nota_1 is None:
                raise HTTPException(status_code=400, detail=f"Falta nota_1 para el estudiante {b.student_id}")
            entry["G1"] = grades.nota_1
        if stage == 3:
            if grades.nota_2 is None:
                raise HTTPException(status_code=400, detail=f"Falta nota_2 para el estudiante {b.student_id}")
            entry["G2"] = grades.nota_2

        data.append(entry)

    df = pd.DataFrame(data)

    # 3. Cargar modelo compacto
    try:
        obj = load_model(stage)   # ahora devuelve el dict con pipe, threshold, classes, feature_names, bg
        pipe = obj["pipe"]
        thr = obj["threshold"]
        classes = obj["classes"]
        i_pos = classes.index("RIESGO ALTO")
        neg = [c for c in classes if c != "RIESGO ALTO"][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando modelo: {str(e)}")

    try:
        # 4. Predicción directa con el pipeline
        p = pipe.predict_proba(df)[:, i_pos]
        y = np.where(p >= thr, "RIESGO ALTO", neg)

        # 5. Configurar LIME
        prep = pipe.named_steps["prep"]
        clf = pipe.named_steps["clf"]

        explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=obj["bg"],                # background ya transformado
            feature_names=obj["feature_names"],     # nombres tras OneHot
            class_names=list(clf.classes_),         # etiquetas reales
            discretize_continuous=True,
            random_state=42
        )

        results = []
        for i, (sid, risk_label) in enumerate(zip(student_ids, y)):
            # Guardar predicción
            risk_entry = PredictedRisk(
                student_id=sid,
                class_id=class_id,
                prediction_stage=stage,
                predicted_risk=risk_label
            )
            db.add(risk_entry)
            db.flush()

            # Explicación: transformar fila antes de LIME
            X_trans = prep.transform(df.iloc[[i]])
            exp = explainer.explain_instance(
                data_row=X_trans[0],
                predict_fn=clf.predict_proba,
                num_features=6
            )
            explanation_dict = exp.as_list()
            explanation_json = json.dumps(explanation_dict)

            explanation_entry = LIMEExplanation(
                predicted_risk_id=risk_entry.id,
                explanation_json=explanation_json
            )
            db.add(explanation_entry)

            results.append({
                "student_id": sid,
                f"predicted_risk_stage_{stage}": risk_label,
                "explanation": explanation_dict
            })

        db.commit()
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {str(e)}")


def get_predictions_by_class_and_stage(class_id: int, stage: int, db: Session):
    results = (
        db.query(PredictedRisk, User, FormResponseBackup)
        .join(User, PredictedRisk.student_id == User.id)
        .join(
            FormResponseBackup, 
            (FormResponseBackup.student_id == PredictedRisk.student_id) &
            (FormResponseBackup.class_id == PredictedRisk.class_id) &
            (FormResponseBackup.prediction_stage == PredictedRisk.prediction_stage)
        )
        .filter(
            PredictedRisk.class_id == class_id,
            PredictedRisk.prediction_stage == stage
        )
        .all()
    )

    enriched_results = []
    for pr, user, backup in results:
        enriched_results.append({
            "student_id": pr.student_id,
            "student_name": user.name,
            "risk": pr.predicted_risk,
            "sex": backup.answer_1,
            "age": int(backup.answer_2) if backup.answer_2 is not None else None,
            "address": backup.answer_3,
            "guardian": backup.answer_4,
            "traveltime": int(backup.answer_5) if backup.answer_5 is not None else None,
            "studytime": int(backup.answer_6) if backup.answer_6 is not None else None,
            "failures": int(backup.answer_7) if backup.answer_7 is not None else None,
            "schoolsup": backup.answer_8,
            "famsup": backup.answer_9,
            "paid": backup.answer_10,
            "activities": backup.answer_11,
            "higher": backup.answer_12,
            "internet": backup.answer_13,
            "romantic": backup.answer_14,
            "famrel": int(backup.answer_15) if backup.answer_15 is not None else None,
            "freetime": int(backup.answer_16) if backup.answer_16 is not None else None,
            "goout": int(backup.answer_17) if backup.answer_17 is not None else None,
            "Dalc": int(backup.answer_18) if backup.answer_18 is not None else None,
            "Walc": int(backup.answer_19) if backup.answer_19 is not None else None,
            "health": int(backup.answer_20) if backup.answer_20 is not None else None,
        })

    return enriched_results


def get_detailed_prediction_explanation_for_student(class_id: int, stage: int, student_id: int, db: Session):
    result = (
        db.query(PredictedRisk, User, FormResponseBackup, LIMEExplanation)
        .join(User, PredictedRisk.student_id == User.id)
        .join(
            FormResponseBackup, 
            (FormResponseBackup.student_id == PredictedRisk.student_id) &
            (FormResponseBackup.class_id == PredictedRisk.class_id) &
            (FormResponseBackup.prediction_stage == PredictedRisk.prediction_stage)
        )
        .join(LIMEExplanation, LIMEExplanation.predicted_risk_id == PredictedRisk.id)
        .filter(
            PredictedRisk.class_id == class_id,
            PredictedRisk.prediction_stage == stage,
            PredictedRisk.student_id == student_id
        )
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="No se encontró información para el estudiante.")

    pr, user, backup, explanation = result

    return {
        "student_id": pr.student_id,
        "student_name": user.name,
        "risk": pr.predicted_risk,
        "lime_explanation": json.loads(explanation.explanation_json),
        "respuestas": {
            "sex": backup.answer_1,
            "age": int(backup.answer_2) if backup.answer_2 is not None else None,
            "address": backup.answer_3,
            "guardian": backup.answer_4,
            "traveltime": int(backup.answer_5) if backup.answer_5 is not None else None,
            "studytime": int(backup.answer_6) if backup.answer_6 is not None else None,
            "failures": int(backup.answer_7) if backup.answer_7 is not None else None,
            "schoolsup": backup.answer_8,
            "famsup": backup.answer_9,
            "paid": backup.answer_10,
            "activities": backup.answer_11,
            "higher": backup.answer_12,
            "internet": backup.answer_13,
            "romantic": backup.answer_14,
            "famrel": int(backup.answer_15) if backup.answer_15 is not None else None,
            "freetime": int(backup.answer_16) if backup.answer_16 is not None else None,
            "goout": int(backup.answer_17) if backup.answer_17 is not None else None,
            "Dalc": int(backup.answer_18) if backup.answer_18 is not None else None,
            "Walc": int(backup.answer_19) if backup.answer_19 is not None else None,
            "health": int(backup.answer_20) if backup.answer_20 is not None else None,
        }
    }

