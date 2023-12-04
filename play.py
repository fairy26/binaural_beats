import time

import flet as ft

frequencies = {
    "δ波": 0.0,
    "θ波": 5.849,
    "α波": 9.498,
    "β波": 26.913,
    "γ波": 34.715,
}


def get_wave_name(frequency_value: float) -> str:
    assert frequency_value >= 0.0
    for key, val in reversed(frequencies.items()):
        if frequency_value >= val:
            return key


def carrier_frequency_picker():
    def slider_changed(e):
        frequency_slider.value = e.control.value
        frequency_slider.update()
        frequency_value_string.value = f"{frequency_slider.value:.3f} Hz"
        frequency_value_string.update()

    def frequency_plus_clicked(e):
        frequency_slider.value += 1.1
        frequency_slider.update()
        frequency_value_string.value = f"{frequency_slider.value:.3f} Hz"
        frequency_value_string.update()

    def frequency_minus_clicked(e):
        frequency_slider.value -= 1.1
        frequency_slider.update()
        frequency_value_string.value = f"{frequency_slider.value:.3f} Hz"
        frequency_value_string.update()

    # Component
    frequency_title = ft.Text("Carrier Frequency")
    frequency_slider = ft.Slider(
        min=21.0,
        max=1200.0,
        value=21.0,
        divisions=1.1,
        label="{value}Hz",
        on_change=slider_changed,
    )
    frequency_value_string = ft.Text(f"{frequency_slider.value:.3f} Hz")

    # TODO: -/+ ボタンは長押しで逐次的に値を変更できるようにしたい
    # on_long_press は発火するのみでオフの扱いがわからん
    frequency_minus_btn = ft.TextButton(
        text="- 0.1[Hz]",
        on_click=frequency_minus_clicked,
    )

    frequency_plus_btn = ft.TextButton(
        text="+ 0.1[Hz]",
        on_click=frequency_plus_clicked,
    )
    return ft.Column(
        [
            ft.Row([frequency_title, frequency_value_string], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.ResponsiveRow(
                [
                    ft.Container(frequency_minus_btn, col={"sm": 2}),
                    ft.Container(frequency_slider, col={"sm": 8}),
                    ft.Container(frequency_plus_btn, col={"sm": 2}),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def beat_frequency_picker():
    def frequency_plus_click(e):
        frequency_changed(float(frequency_slider.value) + 0.1)

    def frequency_minus_click(e):
        frequency_changed(float(frequency_slider.value) - 0.1)

    def slider_changed(e):
        frequency_changed(e.control.value)

    def frequency_selected(e):
        frequency_changed(frequencies[e.control.label.value])

    def frequency_changed(value: float):
        frequency_slider.value = value
        frequency_slider.update()

        wave_name = get_wave_name(frequency_slider.value)
        for chip in frequency_chips.controls:
            chip.selected = chip.label.value == wave_name
        frequency_chips.update()

        frequency_value_string.value = f"{frequency_slider.value:.3f} Hz"
        frequency_value_string.update()

    # Components ----------------------
    frequency_title = ft.Text("Beat Frequency")
    frequency_slider = ft.Slider(
        min=0.0,
        max=40.0,
        value=0.0,
        divisions=0.5,
        label="{value}Hz",
        on_change=slider_changed,
    )
    frequency_value_string = ft.Text(f"{frequency_slider.value:.3f} Hz")

    frequency_chips = ft.Row(
        controls=[
            ft.Chip(
                label=ft.Text(frequency),
                selected=val == frequency_slider.value,
                on_select=frequency_selected,
                show_checkmark=False,
            )
            for frequency, val in frequencies.items()
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    frequency_minus_btn = ft.TextButton(
        text="- 0.1[Hz]",
        on_click=frequency_minus_click,
    )
    frequency_plus_btn = ft.TextButton(
        text="+ 0.1[Hz]",
        on_click=frequency_plus_click,
    )

    area = ft.Column(
        [
            ft.Row([frequency_title, frequency_value_string], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            frequency_chips,
            ft.ResponsiveRow(
                [
                    ft.Container(frequency_minus_btn, col={"sm": 2}),
                    ft.Container(frequency_slider, col={"sm": 8}),
                    ft.Container(frequency_plus_btn, col={"sm": 2}),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return area


def play_btn():
    # ref: https://flet.dev/docs/controls/audio

    def play_btn_clicked(e):
        b.data = not b.data

        # TODO: 再生する

        if b.data:  # now plaing?
            b.text = "Pause"
            b.icon = ft.icons.PAUSE_ROUNDED
        else:
            b.text = "Play"
            b.icon = ft.icons.PLAY_ARROW_ROUNDED
        b.update()

    b = ft.ElevatedButton(
        text="Play",
        icon=ft.icons.PLAY_ARROW_ROUNDED,
        on_click=play_btn_clicked,
        data=False,
    )

    return ft.Row([b], alignment=ft.MainAxisAlignment.CENTER)


def main(page: ft.Page):
    page.title = "Bineural beat / Brain wave"
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.padding = 50
    page.add(
        ft.Divider(),
        carrier_frequency_picker(),
        beat_frequency_picker(),
        play_btn(),
    )


if __name__ == "__main__":
    ft.app(target=main)
