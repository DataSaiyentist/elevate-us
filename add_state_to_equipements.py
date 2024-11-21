import os
import s3fs
import pandas as pd
import numpy as np
from functools import cache
from datetime import datetime
from dateutil.relativedelta import relativedelta

import duckdb as ddb

S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": S3_ENDPOINT_URL})


ddb.execute("SET s3_region='fr-central';")
ddb.execute("SET s3_url_style='path';")
ddb.execute("SET s3_endpoint='minio.data-platform-self-service.net';")
ddb.execute(
    f"SET s3_access_key_id='{os.environ["AWS_ACCESS_KEY_ID"]}' ;"
)  # Aussi récupérable dans les paramètres "Valeurs de Helm" du service
ddb.execute(
    f"SET s3_secret_access_key='{os.environ["AWS_SECRET_ACCESS_KEY"]}';"
)  # Aussi récupérable dans les paramètres "Valeurs de Helm"


def get_history_state_of_equipement(equipement_id) -> datetime:
    limit_date = (datetime.now() - relativedelta(month=6)).strftime("%Y-%m-%d %H:%M:%S")

    history_ascenseur = ddb.sql(
        f""" 
        select * from 's3://dlb-hackathon/datasets-diffusion/ascenseurs_historique_etat/RELEVES_ETATS_ASCENSEURS_SNCF_RATP_2021-2024.parquet'
        where code_appareil = {equipement_id}
        and date_releve >= '{limit_date}'
        """
    ).to_df()

    return (
        history_ascenseur[
            history_ascenseur["etat"] != history_ascenseur["etat"].shift()
        ]
        .assign(
            **{
                "datetime_delta": lambda df: df["date_releve"]
                - df["date_releve"].shift()
            }
        )
        .loc[lambda df: df["etat"] == "1"]["datetime_delta"]
        .mean()
    )


def get_state_from_grievances(equipements) -> pd.Series:
    BUCKET = "dlb-hackathon"
    FILE_KEY_S3 = "equipe-2/grievances.csv"
    FILE_PATH_S3 = BUCKET + "/" + FILE_KEY_S3

    with fs.open(FILE_PATH_S3, mode="r") as file_in:
        grievances = pd.read_csv(file_in)

    states = (
        grievances[grievances["equipement_id"].isin(equipements["id"])]
        .sort_values(by=["equipement_id", "datetime"])
        .groupby("equipement_id")
        .apply(find_state_from_grievances_for_equipement)
    )

CONFIDENCE_THRESHOLD = 10
DATETIME_THRESHOLD = {"positif": np.inf, "negatif": relativedelta(hours=24)}
UNSURE_STATE = {"positif": "positif_incertain", "negatif": "negatif_incertain"}

def find_state_from_grievances_for_equipement(grievances: pd.DataFrame) -> int:
    last_state = grievances.iloc[-1]["state"]
    last_datetime = grievances.iloc[-1]["datetime"]
    nb_identical = (grievances["state"] == last_state).iloc[::-1].cumprod().sum()

    if nb_identical >= CONFIDENCE_THRESHOLD and last_datetime >= DATETIME_THRESHOLD[last_state]:
        return last_state
    else:
        return UNSURE_STATE[last_state]
