function getTags(url) {
    $.ajax({
        url: url,
        method: 'get',
        success: function (json) {
            setPagination(json.prev_page, json.next_page, json.cur_page);
            for (let tag of json.results) {
                $('.tags').append(
                    `<div class="mb-3">
                        <div class="cloud d-flex flex-column p-2">
                            <div class="d-flex">
                                <a href="/search/?q=${encodeURIComponent('[' + tag.name + ']')}">
                                    <div class="blue-cloud me-1 px-2">${tag.name}</div>
                                </a>
                            </div>
                            <div class="d-flex">
                                <p class="mb-0">${tag.reviews_count} reviews</p>
                            </div>
                        </div>
                    </div>`
                );
            }
        }
    });
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
    getTags(`/api/tags/`);
}