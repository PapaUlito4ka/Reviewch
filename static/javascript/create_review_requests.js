function getTags(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            let availableTags = json.data;

            $('#id_tags')
			    .on( 'keydown', function(event) {
                    if (event.keyCode === $.ui.keyCode.TAB &&
                        $(this).autocomplete('instance').menu.active)
                    {
                        event.preventDefault();
                    }
			    })
                .autocomplete({
                    minLength: 0,
                    source: function(request, response) {
                        response($.ui.autocomplete.filter(availableTags, extractLast(request.term)));
                    },
                    focus: function() {
                        return false;
                    },
                    select: function(event, ui) {
                        var terms = split(this.value);
                        terms.pop();
                        terms.push(ui.item.value);
                        terms.push('');
                        this.value = terms.join(' ');
                        return false;
                    }
                });
        }
    });
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

function displayImages() {
    readMultiFiles(this.files);
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
                    console.log(text_markdown);
                    $('.review-text').html(text_markdown);
                }
            });
            cnt = 0;
        }
    }, 500);
}

function split( val ) {
    return val.split( / \s*/ );
}

function extractLast( term ) {
    return split( term ).pop();
}

var cnt = 0;
function render() {
    getTags(`/api/tags/names/`);
    $('#id_images').change(displayImages);
    $('#id_text').keyup(displayText);
}
