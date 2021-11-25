function getReview(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $('.review-author').html(json.author_username);
            $('.review-created-at').html(json.created_at);
            $('.review-group').html(json.group);
            $('.review-title').html(json.title);
            getAuthorImage(`/api/users/${json.author_id}/`, '.review-author-image');

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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getAuthorImage(url, selector) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $(selector).html(
                `<img src="${json.image}" width="20" height="20" alt="img">`
            );
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
                    <a href="#" class="d-flex comment-author-image-${json.id}"></a>
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
            getAuthorImage(`/api/users/${json.author_id}`, `.comment-author-image-${json.id}`);
        }
    });
}

function likeReview(url, reviewId, userId) {
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: url,
        method: 'put',
        data: {
            'user_id': userId
        },
        headers: {'X-CSRFToken': csrftoken },
        success: function (json) {
            $('.review-likes').html(json.data);
            changeLikeReviewButtonIcon(`/api/reviews/${reviewId}/has_liked/?user_id=${userId}`);
        }
    });
}

function changeLikeReviewButtonIcon(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            let likeIcon = $('.review-like-icon');
            if (json.data) {
                likeIcon.removeClass('bi-heart');
                likeIcon.addClass('bi-heart-fill');
            } else {
                likeIcon.removeClass('bi-heart-fill');
                likeIcon.addClass('bi-heart');
            }
        }
    });
}

function rateReview(url, reviewId, userId, rating) {
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: url,
        method: 'put',
        data: {
            'user_id': userId,
            'rating': rating
        },
        headers: {'X-CSRFToken': csrftoken },
        success: function (json) {
            $('.review-average-rating').html(json.data);
            changeRateReviewButtonIcon(`/api/reviews/${reviewId}/has_rated/?user_id=${userId}`);
        }
    })
}

function changeRateReviewButtonIcon(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            if (!json.data) {
                $("input[type='radio']").each(function () {
                    $(this).prop('checked', false);
                });
                return;
            }
            $(`#star${json.data}`).prop('checked', true);
        }
    });
}

function likeComment(url, userId) {
    $.ajax({
        url: url,
        method: 'put',
        data: {
            'user_id': userId
        }
    });
}

function render(reviewId, userId) {
    getReview(`/api/reviews/${reviewId}/`);
    changeLikeReviewButtonIcon(`/api/reviews/${reviewId}/has_liked/?user_id=${userId}`);
    changeRateReviewButtonIcon(`/api/reviews/${reviewId}/has_rated/?user_id=${userId}`);
    $('.like-button').click(function (e) {
        e.preventDefault();
        likeReview(`/api/reviews/${reviewId}/like/`, reviewId, userId);
    });
    $("input[type='radio']").click(function () {
        let rating = $("input[type='radio']:checked").val();
        rateReview(`/api/reviews/${reviewId}/rate/`, reviewId, userId, rating);
    });
}