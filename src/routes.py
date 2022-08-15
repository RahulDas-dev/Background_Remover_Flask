"""Router Module."""

import cv2
from flask import abort, jsonify, request, send_from_directory, url_for

from . import app, ml_model
from .extension import database
from .dbmodel import AddBG, RemoveBG
from .mlmodel.model import add_background_2_img, post_processing_cv2
from .utility import allowed_file


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/blobstore/<name>")
def download_file(name):
    # print(f"asking for download {name}")
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/removebackground", methods=["POST"])
def remove_background():
    # print("Post Request Hit")
    # print(request.files)
    if "file" not in request.files:
        # return jsonify({"upload_status": False, "Fail_reason": "invalid File"})
        abort(404, description="invalid File")
    file = request.files["file"]
    uploadtype_ = request.form["uploadtype"]
    if file.filename == "":
        # return jsonify({"upload_status": False, "Fail_reason": "invalid File"})
        abort(404, description="invalid File Name")
    if allowed_file(file.filename) is False:
        # return jsonify({"upload_status": False, "Fail_reason": "invalid File"})
        abort(404, description="File Extensions are not allowed")
    # print(f"input filename: {file.filename}, uploadtype: {uploadtype_}")
    task = RemoveBG(filename=file.filename, uploadtype=uploadtype_)
    file.save(task.input_image_path)
    input_img = cv2.imread(task.input_image_path)
    mask_img = ml_model.predict(input_img)

    output_img = post_processing_cv2(input_img, mask_img)
    cv2.imwrite(task.output_image_path, output_img)
    cv2.imwrite(task.mask_image_path, mask_img)

    database.session.add(task)
    database.session.commit()
    return jsonify(task.serialize())


@app.route("/addbackground", methods=["POST"])
def add_background():
    # print(request.files)
    if "file" not in request.files:
        # return jsonify({"upload_status": False, "Fail_reason": "invalid File"})
        abort(404, description="invalid File")
    file = request.files["file"]
    task_id_ = request.form["taskid"]
    if file.filename == "":
        # return jsonify({"upload_status": False, "Fail_reason": "invalid File"})
        abort(404, description="invalid File Name")
    if allowed_file(file.filename) is False:
        # return jsonify({"upload_status": False, "Fail_reason": "invalid File"})
        abort(404, description="File Extensions are not allowed")
    parent_task = RemoveBG.query.filter_by(task_id=task_id_).first()
    if parent_task is None:
        # return jsonify({"upload_status": False, "Fail_reason": "invalid File"})
        abort(404, description="Request Not Valid")
    # print(f"task_id: {task_id_}, filename: {file.filename}")
    task = AddBG(taskid=task_id_, filename=file.filename)
    file.save(task.input_image_path)
    # print(f"input_img: {task.input_image_path}, mask_img:{maskname_}, nbg_img:{task.nbg_image_path}")

    input_img = cv2.imread(parent_task.input_image_path)
    mask_img = cv2.imread(parent_task.mask_image_path, cv2.IMREAD_GRAYSCALE)
    nbg_img = cv2.imread(task.input_image_path)
    # Add Code for bg remobval and save it
    bgad_img = add_background_2_img(input_img, mask_img, nbg_img)
    cv2.imwrite(task.output_image_path, bgad_img)
    database.session.add(task)
    database.session.commit()
    return jsonify(task.serialize())
    # return Response(status=200)


@app.route("/workhistory", methods=["GET"])
def get_work_history():
    task_id_ = request.args.get("taskid", default=1, type=int)
    print(f"Post Request Hit {task_id_}")
    # taskList = RMBGMaster.query.all()
    task_list = (
        database.session.query(
            RemoveBG.task_id,
            RemoveBG.upload_date,
            RemoveBG.input_file,
            RemoveBG.mask_file,
            RemoveBG.output_file,
            AddBG.cascade_id,
            AddBG.input_file,
            AddBG.output_file,
        )
        .join(AddBG, RemoveBG.task_id == AddBG.task_id)
        .filter(RemoveBG.task_id > task_id_)
        .order_by(RemoveBG.task_id, AddBG.cascade_id)
        .all()
    )
    return_data = []
    for item in task_list:
        return_data.append(
            {
                "task_id": item[0],
                "upload_date": item[1],
                "input_url": url_for("download_file", name=item[2]),
                "mask_url": url_for("download_file", name=item[3]),
                "output_url": url_for("download_file", name=item[4]),
                "cascade_id": item[5],
                "bg_url": url_for("download_file", name=item[6]),
                "final_url": url_for("download_file", name=item[7]),
            }
        )
    # pprint(returnData)
    return jsonify(return_data)
