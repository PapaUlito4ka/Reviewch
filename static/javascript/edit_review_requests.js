function readURL(event) {
    let input = event.currentTarget;

    readMultiFiles(input.files);
}

function readMultiFiles(files) {
    let reader = new FileReader();
    let images = $('.review-images');
    images.empty();
    function readFile(index) {
        if( index >= files.length ) return;
        let file = files[index];
        reader.onload = function(e) {
            if (index === 0) {
                images.append(
                    `<div class="carousel-item active">
                        <img src="${e.target.result}" class="d-block w-100" alt="...">
                     </div>`
                );
            } else {
                images.append(
                    `<div class="carousel-item">
                        <img src="${e.target.result}" class="d-block w-100" alt="...">
                    </div>`
                );
            }
            readFile(index+1)
        };

        reader.readAsDataURL(file);
    }
    readFile(0);
}

function loadPrevImages(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            let dt = new DataTransfer();
            let cnt = 0;
            for (let i = 0; i < json.images.length; i++) {
                if (i !== json.images.length - 1) {
                   GetFileObjectFromURL(json.images[i], function (imageObj) {
                       dt.items.add(new File([imageObj], 'image.jpg'));
                   });
                } else {
                    GetFileObjectFromURL(json.images[i], function (imageObj) {
                       dt.items.add(new File([imageObj], 'image.jpg'));
                       let imageInput = $('#id_images')[0];
                       imageInput.files = dt.files;
                       readMultiFiles(imageInput.files);
                   });
                }
            }
        }
    })
    
}

function GetFileBlobUsingURL(url, convertBlob) {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.responseType = "blob";
    xhr.addEventListener('load', function() {
        convertBlob(xhr.response);
    });
    xhr.send();
}

function blobToFile(blob, name) {
    blob.lastModifiedDate = new Date();
    blob.name = name;
    return blob;
}

function GetFileObjectFromURL(filePathOrUrl, convertBlob) {
   GetFileBlobUsingURL(filePathOrUrl, function (blob) {
      convertBlob(blobToFile(blob, 'someName.jpg'));
   });
}

function displayText(event) {
    cnt++;
    let counter = cnt;
    setTimeout(function () {
        if (counter === cnt) {
            let text = $('#id_text').val();

            $.ajax({
                url: `/other/text_to_markdown/`,
                method: 'post',
                data: JSON.stringify({
                    'text': text
                }),
                contentType: 'application/json; charset=utf-8',
                success: function (text_markdown) {
                    $('.review-text').html(text_markdown);
                }
            });
            cnt = 0;
        }
    }, 500);
}

var cnt = 0;
function render(id) {
    displayText(null);
    $('#id_images').change(readURL);
    $('#id_text').keyup(displayText);
    loadPrevImages(`/api/reviews/${id}`);
}
