from db import db, TimeRecord


def prepare():
    for gender in range(1, 3):
        for floor in range(1, 11):
            for hour_distance in range(11):
                hour = str((22 + hour_distance) % 24)
                if len(hour) < 2:
                    hour = "0" + hour
                for minutes_int in range(0, 31, 30):
                    minutes = str(minutes_int)
                    if len(minutes) < 2:
                        minutes = "0" + minutes
                    new_record = TimeRecord(
                        floor=floor,
                        record_time=(hour + ":" + minutes),
                        username="-",
                        username_second="-",
                        gender=gender,
                    )
                    db.add(new_record)
                    db.commit()
    db.close()


if __name__ == "__main__":
    prepare()
