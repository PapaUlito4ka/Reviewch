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

function getUserReview(url, i) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (review) {
            $(`.table-review-${review.id}`).append(
                `<tr>
                    <th scope="row" class="text-center">${i + 1}</th>
                    <td class="text-center">${review.group}</td>
                    <td class="text-center">${review.title}</td>
                    <td class="d-flex flex-row justify-content-around align-items-center">
                        <a href="#" class="h5 m-0"><i class="bi bi-eye"></i></a>
                        <a href="#" class="h5 m-0"><i class="bi bi-pencil-square"></i></a>
                        <a href="#" class="h5 m-0"><i class="bi bi-trash"></i></a>
                    </td>
                </tr>`
            )
        }
    })
}

function getUserReviews(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            if (json.reviews.length !== 0) {
                $('.reviews-table').find('tbody').find(':first-child').remove();
            }
            else {
                $('.reviews-table').remove();
                $('.reviews-cloud').append('<p class="text-center">No publications here yet</p>')
            }
            for (let i = 0; i < json.reviews.length; i++) {
                $('.reviews-table').append(
                    `<tbody class="table-review-${json.reviews[i]}">
                    </tbody>`
                );
                getUserReview(`/api/reviews/${json.reviews[i]}/`, i);
            }
        }
    })
}


function render(userId) {
    getUserPublicationsCount(`/api/users/${userId}/publications_count`);
    getUserAverageRating(`/api/users/${userId}/average_rating`);
    getUserTotalLikes(`/api/users/${userId}/total_likes`);
    getUserCommentsCount(`/api/users/${userId}/comments_count`);
    getUserReviews(`/api/users/${userId}`);
}

