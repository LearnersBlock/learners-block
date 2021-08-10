from common.models import App_Store


# Used by the application store functions to update status of application
def update_container_db_status(name, status):
    # Fetch database entry based on passed name
    lb_database = App_Store.query.filter_by(
        name=name).first()

    # Update and return
    lb_database.status = status
    lb_database.save_to_db()
