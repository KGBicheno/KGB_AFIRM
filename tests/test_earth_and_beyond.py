import discord.ext.test as dpytest
import pytest


class TestEarthAndBeyond:

    @pytest.mark.asyncio
    async def test_woah_with_ok_response(self, bot, aresponses):
        # given
        response = {
            "copyright": "Joonhwa Lee",
            "date": "2020-05-01",
            "explanation": "Big, bright, beautiful spiral, Messier 106 dominates this cosmic vista. [truncated]",
            "hdurl": "https://apod.nasa.gov/apod/image/2005/M106_ORG4_APOD.jpg",
            "media_type": "image",
            "service_version": "v1",
            "title": "A View Toward M106",
            "url": "https://apod.nasa.gov/apod/image/2005/M106_ORG4_APOD1024c.jpg"
        }
        aresponses.add("api.nasa.gov", "/planetary/apod", "GET", response)

        # when
        message_help = await dpytest.message("%woah")

        # then
        assert message_help.content == '%woah'

        message_count = dpytest.sent_queue.qsize()
        assert message_count == 3

        message_aligning_mirrors = dpytest.sent_queue.get_nowait()
        assert message_aligning_mirrors.content == 'Aligning mirrors ...'

        message_capture_state = dpytest.sent_queue.get_nowait()
        assert message_capture_state.content == 'Setting capture state ...'

        message_capture_state = dpytest.sent_queue.get_nowait()
        assert message_capture_state.content is None
        assert message_capture_state.embeds is not None
        assert len(message_capture_state.embeds) == 1
        assert message_capture_state.embeds[0].author.name == response['copyright']
        assert message_capture_state.embeds[0].image.url == response['url']

        aresponses.assert_plan_strictly_followed()

    @pytest.mark.asyncio
    async def test_mars_with_ok_response(self, bot, aresponses):
        # given
        response = {"photos": [{"id": 102693, "sol": 1000, "camera": {"id": 20, "name": "FHAZ", "rover_id": 5,
                                                                      "full_name": "Front Hazard Avoidance Camera"},
                                "img_src": "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FLB_486265257EDR_F0481570FHAZ00323M_.JPG",
                                "earth_date": "2015-05-30",
                                "rover": {"id": 5, "name": "Curiosity", "landing_date": "2012-08-06",
                                          "launch_date": "2011-11-26", "status": "active", "max_sol": 2791,
                                          "max_date": "2020-06-12", "total_photos": 426678,
                                          "cameras": [{"name": "FHAZ", "full_name": "Front Hazard Avoidance Camera"},
                                                      {"name": "NAVCAM", "full_name": "Navigation Camera"},
                                                      {"name": "MAST", "full_name": "Mast Camera"},
                                                      {"name": "CHEMCAM", "full_name": "Chemistry and Camera Complex"},
                                                      {"name": "MAHLI", "full_name": "Mars Hand Lens Imager"},
                                                      {"name": "MARDI", "full_name": "Mars Descent Imager"},
                                                      {"name": "RHAZ", "full_name": "Rear Hazard Avoidance Camera"}]}},
                               {"id": 102694, "sol": 1000, "camera": {"id": 20, "name": "FHAZ", "rover_id": 5,
                                                                      "full_name": "Front Hazard Avoidance Camera"},
                                "img_src": "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FRB_486265257EDR_F0481570FHAZ00323M_.JPG",
                                "earth_date": "2015-05-30",
                                "rover": {"id": 5, "name": "Curiosity", "landing_date": "2012-08-06",
                                          "launch_date": "2011-11-26", "status": "active", "max_sol": 2791,
                                          "max_date": "2020-06-12", "total_photos": 426678,
                                          "cameras": [{"name": "FHAZ", "full_name": "Front Hazard Avoidance Camera"},
                                                      {"name": "NAVCAM", "full_name": "Navigation Camera"},
                                                      {"name": "MAST", "full_name": "Mast Camera"},
                                                      {"name": "CHEMCAM", "full_name": "Chemistry and Camera Complex"},
                                                      {"name": "MAHLI", "full_name": "Mars Hand Lens Imager"},
                                                      {"name": "MARDI", "full_name": "Mars Descent Imager"},
                                                      {"name": "RHAZ", "full_name": "Rear Hazard Avoidance Camera"}]}}]}
        aresponses.add("api.nasa.gov", "/mars-photos/api/v1/rovers/curiosity/photos", "GET", response)

        # when
        message_help = await dpytest.message("%mars")

        # then
        assert message_help.content == '%mars'

        message_count = dpytest.sent_queue.qsize()
        assert message_count == 8

        # go through the 6 text messages
        for index in range(6):
            text_message = dpytest.sent_queue.get_nowait()
            assert text_message.content is not None

        # left photo
        message_left = dpytest.sent_queue.get_nowait()
        assert message_left.content == response['photos'][0]['img_src']

        # right photo
        message_right = dpytest.sent_queue.get_nowait()
        assert message_right.content == response['photos'][1]['img_src']

        aresponses.assert_plan_strictly_followed()

    @pytest.mark.asyncio
    async def test_woah_with_error_response(self, bot, aresponses):
        # given
        aresponses.add("api.nasa.gov", "/planetary/apod", "GET", aresponses.Response(status=404))

        # when
        message_help = await dpytest.message("%woah")

        # then
        assert message_help.content == '%woah'

        message_count = dpytest.sent_queue.qsize()
        assert message_count == 3

        message_aligning_mirrors = dpytest.sent_queue.get_nowait()
        assert message_aligning_mirrors.content == 'Aligning mirrors ...'

        message_capture_state = dpytest.sent_queue.get_nowait()
        assert message_capture_state.content == 'Setting capture state ...'

        message_capture_state = dpytest.sent_queue.get_nowait()
        assert message_capture_state.content == "I'm very sorry, I'm looking up at the expanse " \
                                                "of the universe just now. " \
                                                "I might be able to show another snapshot " \
                                                "of the wonder a little later."

        aresponses.assert_plan_strictly_followed()
