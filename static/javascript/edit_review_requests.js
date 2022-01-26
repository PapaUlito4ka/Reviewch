function readURL(event) {
    let input = event.currentTarget;
    $('.display-images').empty();

    readMultiFiles(input.files);
}

function readMultiFiles(files) {
    let reader = new FileReader();
    function readFile(index) {
        if( index >= files.length ) return;
        let file = files[index];
        reader.onload = function(e) {
            $('.display-images').append(
                `<img id="image" src="${e.target.result}" alt="image" class="img-fluid" />`
            );
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
                       dt.items.add(new File([imageObj], 'image'));
                   });
                } else {
                    GetFileObjectFromURL(json.images[i], function (imageObj) {
                       dt.items.add(new File([imageObj], 'image'));
                       let imageInput = $('#id_images');
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


function render(id) {
    $('#id_images').change(readURL);
    loadPrevImages(`/api/reviews/${id}`);
}
