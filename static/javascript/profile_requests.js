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

function getUserPublicationsCount(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $('.publication-count').html(json.data);
        }
    });
}

function getUserAverageRating(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $('.average-rating').text(json.data);
        }
    });
}

function getUserTotalLikes(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $('.total-likes').text(json.data);
        }
    });
}

function getUserCommentsCount(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $('.comments-count').text(json.data);
        }
    });
}

function getUser(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $('.user-username').html(json.username);
            $('.profile-image').prop('src', json.image);
        }
    });
}

function getUserReviews(url, userId, userIsStaff) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            setPagination(json.prev_page, json.next_page, json.cur_page);
            if (json.results.length !== 0) {
                $('.reviews-table').find('tbody').find(':first-child').remove();
            }
            else {
                $('.reviews-table').find('tbody').remove();
                $('.reviews-cloud').append('<p class="text-center">No publications here yet</p>');
            }
            let i = 0;
            for (let review of json.results) {
                $('.reviews-table').append(
                    `<tbody class="table-review-${review.id}">
                    </tbody>`
                );

                let cond = review.author_id !== userId && !userIsStaff;
                $(`.table-review-${review.id}`).append(
                    `<tr>
                        <th scope="row" class="text-center">${i + 1}</th>
                        <td class="text-center">${review.group}</td>
                        <td class="text-center">${review.title.length > 32 ? review.title.slice(0, 32) + '...' : review.title}</td>
                        <td class="d-flex flex-row justify-content-around align-items-center">
                            <a href="/review/${review.id}/" class="h5 m-0"><i class="bi bi-eye"></i></a>
                            <a href="/edit_review/${review.id}/" class="h5 m-0" ${cond ? 'hidden' : ""}><i class="bi bi-pencil-square"></i></a>
                            <a href="#" class="h5 m-0" ${cond ? 'hidden' : ""} onclick="deleteReviewDialog(${review.id}, ${userId})"><i class="bi bi-trash"></i></a>
                        </td>
                    </tr>`
                );
                i++;
            }
        }
    });
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

function findUserReviews(search, userSessionId, userIsStaff, userId, ordering, group, page) {
    let [query, parsedQuery] = parseSearchQuery(search);
    $('.reviews-cloud').find('p').remove();
    $('.reviews-table').find('tbody').remove();
    $('.reviews-table').append(
        `<tbody>
            <tr>
                <th scope="col" class="text-center">Loading...</th>
                <th scope="col" class="text-center">Loading...</th>
                <th scope="col" class="text-center">Loading...</th>
                <th scope="col" class="text-center">Loading...</th>
            </tr>
        </tbody>`
    );
    getUserReviews(
        `/api/reviews/?author__id=${userId}&search=${query}&ordering=${ordering}&group=${group}&page=${page}${parsedQuery}`,
        userSessionId,
        userIsStaff
    );
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

function deleteReview(url, userId) {
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: url,
        method: 'delete',
        headers: {'X-CSRFToken': csrftoken },
        success: function (json) {
            window.location.href = `/profile/${userId}`
        }
    });
}

function deleteReviewDialog(reviewId, userId) {
    let res = confirm('You sure you want to delete selected review?');
    if (res)
        deleteReview(`/api/reviews/${reviewId}/`, userId);
}

function render(userSessionId, userId, userIsStaff, search, ordering, group, page) {
    getUserPublicationsCount(`/api/users/${userId}/publications_count`);
    getUserAverageRating(`/api/users/${userId}/average_rating`);
    getUserTotalLikes(`/api/users/${userId}/total_likes`);
    getUserCommentsCount(`/api/users/${userId}/comments_count`);
    findUserReviews(search, userSessionId, userIsStaff, userId, ordering, group, page);
    getUser(`/api/users/${userId}`);

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

    $('#profile-search').keypress(function (e) {
        if (e.which === 13) {
            findUserReviews(e.target.value, userSessionId, userIsStaff, userId, ordering, group, page);
        }
    });
}

