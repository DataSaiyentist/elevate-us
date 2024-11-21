# Installation des dépendances :
import pandas as pd
import s3fs
import os

# !pip install s3fs

# import des dépendances

# Creation d'un objet filesystem, les variables d'environnement on été automatiquement traitées par Onyxia
S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": S3_ENDPOINT_URL})


def add_grievances(equipment_id, datetime, state, commentaire):

    df = pd.DataFrame(data={"equipment_id": equipment_id,
                            "datetime": datetime, "state": state, "commentaire": commentaire}, index=[0])

    # Ecrire
    BUCKET_OUT = "dlb-hackathon"
    FILE_KEY_OUT_S3 = "equipe-2/grievances.csv"
    FILE_PATH_OUT_S3 = BUCKET_OUT + "/" + FILE_KEY_OUT_S3

    with fs.open(FILE_PATH_OUT_S3, "a") as file_out:
        df.to_csv(file_out, header=None)


# add_grievances(1038, "2024-11-21T18:08:00", "negatif",
#                "ascenseur il est tout cassé")

# add_grievances(1038, "2024-11-21T18:11:00", "negatif",
#                "ascenseur il est tout cassé")

# add_grievances(1038, "2024-11-21T18:20:00", "negatif",
#                "ascenseur il est tout cassé")

add_grievances(1038, "2024-11-21T18:40:00", "positif",
               "ascenseur il est bien")

add_grievances(1038, "2024-11-21T18:40:00", "positif",
               "ascenseur il est bien")

# add_grievances(318, "2024-11-21T18:11:00", "negatif",
#                "marche pas")

# add_grievances(1156, "2024-11-21T18:11:00", "negatif",
#                "marche pas")

# add_grievances(1681522, "2024-11-21T18:11:00", "negatif",
#                "escalator recule au lieu d'avancer")

# add_grievances(1681522, "2024-11-21T18:11:00", "negatif",
#                "escalatueur recule au lieu d'avancer")
