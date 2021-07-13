function compress_base64(ev, submit_input, append_form, MAX_WIDTH, MAX_HEIGHT, MIME_TYPE, QUALITY) {
    const file = ev.target.files[0];
    const blobURL = URL.createObjectURL(file);
    const img = new Image();
    img.src = blobURL;
    img.onerror = function() {
        URL.revokeObjectURL(this.src);
        // Handle the failure properly
        console.log("Cannot load image");
        return 'no-image'
    };

    img.onload = function() {
        URL.revokeObjectURL(this.src);
        const [newWidth, newHeight] = calculateSize(img, MAX_WIDTH, MAX_HEIGHT);
        const canvas = document.createElement("canvas");
        canvas.width = newWidth;
        canvas.height = newHeight;
        canvas.display = 'none';

        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, newWidth, newHeight);
        canvas.toBlob(
            (blob) => {
                // Handle the compressed image. es. upload or save in local state
                var reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = function() {
                    var base64String = reader.result;
                    submit_input.value = base64String;
                }

            },
            MIME_TYPE,
            QUALITY
        );
        append_form.append(canvas);
    };
};

function calculateSize(img, maxWidth, maxHeight) {
    let width = img.width;
    let height = img.height;

    // calculate the width and height, constraining the proportions
    if (width > height) {
        if (width > maxWidth) {
            height = Math.round((height * maxWidth) / width);
            width = maxWidth;
        }
    } else {
        if (height > maxHeight) {
            width = Math.round((width * maxHeight) / height);
            height = maxHeight;
        }
    }
    return [width, height];
}