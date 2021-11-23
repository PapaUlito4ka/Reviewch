function getReview(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $('.review-author').html(json.author_username);
            $('.review-created-at').html(json.created_at);
            $('.review-group').html(json.group);
            $('.review-title').html(json.title);

            $('.review-tags').find(':first-child').remove();
            for (let i = 0; i < json.tags.length; i++) {
                $('.review-tags').append(
                    `<a href="#"><div class="blue-cloud me-1 px-2">${json.tags[i]}</div></a>`
                );
            }

            $('.review-text').html(json.text);
            if (json.images.length === 0) {
                $('.review-carousel').remove();
            }
            for (let i = 0; i < json.images.length; i++) {
                if (i === 0) {
                    $('.review-images').append(
                        `<div class="carousel-item active">
                        <img src="${json.images[i]}" class="d-block w-100" alt="...">
                    </div>`
                    );
                } else {
                    $('.review-images').append(
                        `<div class="carousel-item">
                        <img src="${json.images[i]}" class="d-block w-100" alt="...">
                    </div>`
                    );
                }
            }
            $('.review-average-rating').html(json.average_rating);
            $('.review-likes').html(json.likes);

            if (json.comments.length === 0) {
                $('.review-comments').find(':first-child').html('No comments');
            }
            else {
                $('.review-comments').find(':first-child').remove();
            }
            for (let i = 0; i < json.comments.length; i++) {
                $('.review-comments').append(`<div class="review-comment-${json.comments[i]}"></div>`)
                getReviewComment(`/api/comments/${json.comments[i]}/`);
            }
        }
    });
}

function getReviewComment(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $(`.review-comment-${json.id}`).append(
                `<div class="d-flex flex-row align-items-center mb-2">
                    <a href="#" class="d-flex"><img src="{% get_media_prefix %}user_profile.png" width="20" height="20"></a>
                    <a href="#" class="m-0 mx-2">${json.author_username}</a>
                    <p class="m-0 mx-2 text-secondary">${json.created_at}</p>
                </div>
                <div class="d-flex flex-column mb-2">
                    <p class="m-0">${json.text}</p>
                </div>
                <div class="d-flex flex-row mb-2 align-items-center">
                    <span class="h3 m-0 me-2"><i class="bi bi-heart p-0"></i></span>
                    <span class="p-0">${json.likes}</span>
                </div>`
            );
        }
    });
}

function render(reviewId) {
    getReview(`/api/reviews/${reviewId}/`);
}