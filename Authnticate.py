@app.route('/get_patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients WHERE patient_id=%s", (patient_id,))
    patient = cursor.fetchone()

    if patient:
        return {
            "patient_id": patient[0],
            "name": patient[1],
            "date_of_birth": patient[2],
            "gender": patient[3],
            "address": patient[4],
            "s3_key": patient[5],
            "file_url": s3_client.generate_presigned_url('get_object', Params={'Bucket': 'my-healthcare-data', 'Key': patient[5]}, ExpiresIn=3600)
        }
    else:
        return "Patient not found", 404
