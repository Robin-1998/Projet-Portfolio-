"""
@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']  # depuis un formulaire HTML ou JS
    title = request.form['title']
    description = request.form['description']
    user_id = int(request.form['user_id'])

    image_data = file.read()
    mime_type = file.mimetype  # ex: "image/jpeg"

    image_post = ImagePost(
        title=title,
        description=description,
        image_data=image_data,
        image_mime_type=mime_type,
        user_id=user_id
    )
    db.session.add(image_post)
    db.session.commit()

    return jsonify(image_post.to_dict()), 201


@app.route('/image/<int:image_id>')
def get_image(image_id):
    image_post = db.session.get(ImagePost, image_id)
    if not image_post:
        return "Not found", 404
    return Response(image_post.image_data, mimetype=image_post.image_mime_type)


"""
