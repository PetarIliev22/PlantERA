
def get_device_models(client):
    response = (
        client.table("device_models")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data
