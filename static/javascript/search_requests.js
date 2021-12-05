function getReviews(url, userId) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            setPagination(json.prev_page, json.next_page, json.cur_page);
            for (let review of json.results) {
                $('.reviews').append(
                    `<div class="cloud mt-3">
                        <div class="row px-4 py-3">
                            <div class="d-flex flex-row align-items-center mb-2">
                                <a href="/profile/${review.author_id}" class="d-flex review-${review.id}-author-image">Loading...</a>
                                <a href="/profile/${review.author_id}" class="m-0 mx-2 review-${review.id}-author">Loading...</a>
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
                                <a href="/review/${review.id}/"><div class="blue-cloud"><i class="bi bi-arrow-right-short h2"></i></div></a>
                                <div class="d-flex flex-row align-items-center">
                                    <span class="h3 m-0 me-2"><i class="bi bi-star p-0 review-${review.id}-star"></i></span>
                                    <span class="p-0 me-4 review-${review.id}-average-rating">Loading...</span>
                                    <span class="h3 m-0 me-2"><i class="bi bi-heart p-0 review-${review.id}-heart"></i></span>
                                    <span class="p-0 review-${review.id}-likes">Loading...</span>
                                </div>
                            </div>
                        </div>
                    </div>`
                );
                getReview(review, userId);
            }
            if (json.results.length === 0) {
                $('.reviews').addClass('cloud mt-3');
                $('.reviews').append(
                    `<p class="text-center">No content</p>`
                );
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
            `<a href="/search/?q=${encodeURIComponent('[' + review.tags[i] + ']')}"><div class="blue-cloud me-1 px-2">${review.tags[i]}</div></a>`
        );
    }

    if (review.text.length > 200)
        $(`.review-${review.id}-text`).html(review.text_markdown.slice(0, 200) + '...');
    else
        $(`.review-${review.id}-text`).html(review.text_markdown);
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

function setUrlParameter(name, value) {
    const url = new URLSearchParams(window.location.search);
    if (url.has(name)) {
        if (url.get(name) === value) {
            url.delete(name);
        } else url.set(name, value);
    } else {
        url.set(name, value);
    }
    window.location.search = url;
}

function parseSearchQuery(query) {
    let tags_query = '';
    let open = query.indexOf('[', 0);
    while (open !== -1) {
        let close = query.indexOf(']', open);
        if (close === -1) break;
        tags_query += '&tags__name=' + query.slice(open + 1, close);
        query = query.slice(0, open) + query.slice(close + 1);
        open = query.indexOf('[', open);
    }
    let user_query = '';
    open = query.indexOf('(user:', 0);
    if (open !== -1) {
        close = query.indexOf(')', open + 6);
        user_query += '&author__id=' + query.slice(open + 6, close);
        query = query.slice(0, open) + query.slice(close + 1);
    }
    return [query, tags_query + user_query];
}

function setPagination(prevPage, nextPage, curPage) {
    if (prevPage)
        $('.prev-page').prop('href', `?page=${prevPage}`);
    else
        $('.prev-page').remove();
    if (nextPage)
        $('.next-page').prop('href', `?page=${nextPage}`);
    else
        $('.next-page').remove();
    $('.cur-page').html(curPage);
}

function render(userId, search, ordering, group, page) {
    let [query, parsedQuery] = parseSearchQuery(search);
    getReviews(`/api/reviews/?search=${query}&ordering=${ordering}&group=${group}&page=${page}${parsedQuery}`, userId);
    $('.latest-order').click(function () {
        setUrlParameter('ordering', '-created_at')
    });
    $('.rating-order').click(function () {
        setUrlParameter('ordering', '-average_rating')
    });
    $('.movies-group').click(function () {
        setUrlParameter('group', 'Movies')
    });
    $('.games-group').click(function () {
        setUrlParameter('group', 'Games')
    });
    $('.books-group').click(function () {
        setUrlParameter('group', 'Books')
    });
    $('.music-group').click(function () {
        setUrlParameter('group', 'Music')
    });
    $('.art-group').click(function () {
        setUrlParameter('group', 'Art')
    });
}