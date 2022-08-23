import pytest

from service import service


class TestService:

    @pytest.mark.parametrize(
        'page_count, expected',
        [(20, [1]), (44, [3, 2, 1]), (98, [5, 4, 3, 2, 1])]
    )
    def test_get_page_list(self, page_count, expected):
        result = service.get_page_list(page_count)
        assert result == expected

    def test_get_link_mirror(self):
        link = 'https://animevost.org/tip/tv/test.html'
        result = service.get_link_mirror(link)
        assert result == 'https://v2.vost.pw/tip/tv/test.html'

    def test_get_link_mirror_not_link(self):
        link = 'https://test.org/tip/tv/test.html'
        result = service.get_link_mirror(link)
        assert result == link

    def test_get_image(self):
        url_image_preview = 'https://test.jpg'
        telegram_id_file = 'QWERT'
        result = service.get_image(url_image_preview, telegram_id_file)
        assert result == telegram_id_file

    def test_get_image_not_telegram_id_file(self):
        url_image_preview = 'https://test.jpg'
        result = service.get_image(url_image_preview, None)
        assert result == url_image_preview
