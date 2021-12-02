function getUsers(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            setPagination(json.prev_page, json.next_page, json.cur_page);
            for (let user of json.results) {
                $('.users').append(
                    `<div class="mb-3">
                        <div class="cloud d-flex flex-column p-2">
                            <div class="d-flex">
                                <img src="${user.image}" class="rounded me-2" width="50" height="50">
                                <div class="flex-fill align-self-end">
                                    <div class="d-flex align-items-center">
                                        <span class="me-2"><a href="/profile/${user.id}">${user.username}</a></span>
                                    </div>
                                    <div class="d-flex align-items-center">
                                        <span class="h5 m-0 me-1"><i class="bi bi-star p-0"></i></span>
                                        <span class="p-0 me-2 user-${user.id}-average-rating">Loading...</span>
                                        <span class="h5 m-0 me-1"><i class="bi bi-heart p-0"></i></span>
                                        <span class="p-0 user-${user.id}-likes">Loading...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`
                );
                getUserAverageRating(`/api/users/${user.id}/average_rating/`, user.id);
                getUserTotalLikes(`/api/users/${user.id}/total_likes/`, user.id);
            }
            if (json.results.length === 0) {
                // $('.users').addClass('cloud mt-3');
                $('.users').append(
                    `<p class="text-center">No content</p>`
                );
            }
        }
    });
}

function getUserAverageRating(url, userId) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $(`.user-${userId}-average-rating`).html(json.data);
        }
    });
}

function getUserTotalLikes(url, userId) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            $(`.user-${userId}-likes`).html(json.data);
        }
    });
}

function findUsers(search) {
    getUsers(`/api/users?search=${search}`);
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

function render() {
    getUsers(`/api/users/`);
    $('#users-search').keypress(function(e) {
        if (e.which === 13) {
            $('.users').empty();
            findUsers(e.target.value);
        }
    });
}