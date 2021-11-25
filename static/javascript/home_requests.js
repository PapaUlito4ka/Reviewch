function getReviews(url, userId) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {

            for (let review of json) {
                $('.reviews').append(
                    `<div class="row px-4 py-3">
                        <div class="d-flex flex-row align-items-center mb-2">
                            <a href="#" class="d-flex review-${review.id}-author-image">Loading...</a>
                            <a href="#" class="m-0 mx-2 review-${review.id}-author">Loading...</a>
                            <p class="m-0 mx-2 text-secondary review-${review.id}-created-at">Loading...</p>
                        </div>
                        <div class="d-flex flex-row mb-2">
                            <p class="m-0 fst-italic h4 review-${review.id}-group">Loading...</p>
                        </div>
                        <div class="d-flex flex-row mb-2">
                            <p class="m-0 fw-bold h4 review-${review.id}-title">Loading...</p>
                        </div>
                        <div class="d-flex flex-row mb-2 review-${review.id}-tags">
                        </div>
                        <div class="d-flex flex-column mb-2 review-${review.id}-text">
                            <p class="m-0">Loading...</p>
                        </div>
                        <div class="d-flex flex-row justify-content-between">
                            <a href="/review/${review.id}/"><div class="blue-cloud p-2 px-4">Read</div></a>
                            <div class="d-flex flex-row align-items-center">
                                <span class="h3 m-0 me-2"><i class="bi bi-star p-0 review-${review.id}-star"></i></span>
                                <span class="p-0 me-4 review-${review.id}-average-rating">Loading...</span>
                                <span class="h3 m-0 me-2"><i class="bi bi-heart p-0 review-${review.id}-heart"></i></span>
                                <span class="p-0 review-${review.id}-likes">Loading...</span>
                            </div>
                        </div>
                    </div>`
                );
                getReview(review, userId);
            }
        }
    });
}

function getReview(review, userId) {
    $(`.review-${review.id}-author`).html(review.author_username);
    $(`.review-${review.id}-created-at`).html(review.created_at);
    $(`.review-${review.id}-group`).html(review.group);
    $(`.review-${review.id}-title`).html(review.title);
    getAuthorImage(`/api/users/${review.author_id}/`, `.review-${review.id}-author-image`);

    let tags = $(`.review-${review.id}-tags`);
    tags.find(':first-child').remove();
    for (let i = 0; i < review.tags.length; i++) {
        tags.append(
            `<a href="#"><div class="blue-cloud me-1 px-2">${review.tags[i]}</div></a>`
        );
    }

    $(`.review-${review.id}-text`).html(review.text);
    $(`.review-${review.id}-average-rating`).html(review.average_rating);
    $(`.review-${review.id}-likes`).html(review.likes);
    if (userId) {
        changeLikeReviewButtonIcon(`/api/reviews/${review.id}/has_liked/?user_id=${userId}`, review.id);
        changeRateReviewButtonIcon(`/api/reviews/${review.id}/has_rated/?user_id=${userId}`, review.id);
    }
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

function changeLikeReviewButtonIcon(url, reviewId) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            let likeIcon = $(`.review-${reviewId}-heart`);
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

function changeRateReviewButtonIcon(url, reviewId) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            let starIcon = $(`.review-${reviewId}-star`);
            if (json.data) {
                starIcon.removeClass('bi-star');
                starIcon.addClass('bi-star-fill');
            } else {
                starIcon.removeClass('bi-star-fill');
                starIcon.addClass('bi-star');
            }
        }
    });
}

function render(userId, ordering, group) {
    getReviews(`/api/reviews/?ordering=${ordering}&group=${group}`, userId);
}