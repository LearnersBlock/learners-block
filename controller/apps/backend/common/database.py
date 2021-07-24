from common.models import App_Store


def update_container_db_status(name, status):
    try:
        lb_database = App_Store.query.filter_by(
            name=name).first()

        lb_database.status = status

        lb_database.save_to_db()
    except Exception as ex:
        print("update_container_db_status - " + str(ex))
        return {'message': "update_container_db_status - " + str(ex)}, 500

    return {'message': 'done'}, 200
