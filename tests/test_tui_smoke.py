import pytest

from kcna.tui.app import ExamApp


@pytest.mark.asyncio
async def test_exam_app_boots_to_title():
    app = ExamApp(seed=7)
    async with app.run_test() as pilot:
        await pilot.pause()
        from kcna.tui.screens.title import TitleScreen

        assert isinstance(app.screen, TitleScreen)


@pytest.mark.asyncio
async def test_exam_screen_ignores_escape_and_advances_on_letter():
    app = ExamApp(seed=7)
    async with app.run_test() as pilot:
        await pilot.press("s")
        await pilot.pause()

        from kcna.tui.screens.exam import ExamScreen

        assert isinstance(app.screen, ExamScreen)
        screen = app.screen
        start_index = screen._index

        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, ExamScreen)
        assert screen._index == start_index

        await pilot.press("a")
        await pilot.pause()
        assert screen._index == start_index + 1


@pytest.mark.asyncio
async def test_finish_exam_reaches_results():
    app = ExamApp(seed=7)
    async with app.run_test() as pilot:
        await pilot.press("s")
        await pilot.pause()
        for _ in range(65):
            await pilot.press("a")
            await pilot.pause()

        from kcna.tui.screens.results import ResultsScreen

        assert isinstance(app.screen, ResultsScreen)
