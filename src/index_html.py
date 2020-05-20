html = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
    <head> <title>Neopixel googles configuration</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
            body {{
                background-color: linen;
            }}

            h1 {{
                color: maroon;
                margin-left: 40px;
            }}
            main {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}

            .control {{
                display: flex;
                justify-content: flex-start;
                margin-bottom: 2em;
            }}
        </style>
    </head>
    <body>
    <main>
    <header>
        <h1>Configuration page</h1>
        <h2>You can choose program and color</h2>
    </header>
            <section class="control program-control">
                <input type="radio" name="program" value="1" {is1checked}> Cycle
                <input type="radio" name="program" value="2" {is2checked}> Bounce
                <input type="radio" name="program" value="3" {is3checked}> Fade
                <input type="radio" name="program" value="4" {is4checked}> Rainbow
                <input type="radio" name="program" value="5" {is5checked}> Crazy Rainbow
                <input type="radio" name="program" value="6" {is6checked}> Gradient
            </section>
            <section class="control color-control">
                Active color: <input type="color" name="color" value="#{color}">
                Background color: <input type="color" name="background_color" value="#{background_color}">
            </section>
            <section class="control delay-control">
                Animation delay: <input type="range" list="tickmarks" name="delay" min=5 max=500 step=5 value="100">
                <datalist id="tickmarks">
                    <option value="5" label="min"></option>
                    <option value="100" label="default"></option>
                    <option value="500" label="max"></option>
                </datalist>
            </section>
            <section class="control hardware-control">
              Number of LEDS: <input type="number" name="led_amount" min="1" max="32" value="{led_amount}">
              Number of Bits: <input type="number" name="led_bits" min="3" max="4" value="{led_bits}">
              <small>*require restart</small>
              Timer delta: <input type="number" name="delta_time" value="{delta_time}">
            </section>
        </main>
        <script>
            async function onChange(e) {{
                try {{
                    const value = e.target.value;
                    const param = e.target.name;
                    result = await fetch('/', {{
                        method: 'POST',
                        body: JSON.stringify({{[param]: value}})
                    }})
                }} catch (error) {{
                    e.preventDefault();
                    console.error(error);
                    alert("Something went wrong, check console for details!");
                }}
            }}
            document.querySelectorAll("input").forEach(
                (el) => el.addEventListener('change', (e) => onChange(e))
            );
        </script>
    </body>
</html>
"""
