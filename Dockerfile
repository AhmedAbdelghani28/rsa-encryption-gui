FROM python:3.11-slim

# Qt6 / X11 runtime libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Qt6 core runtime
    libdouble-conversion3 \
    libmd4c0 \
    libpcre2-16-0 \
    libharfbuzz0b \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    zlib1g \
    libzstd1 \
    libicu72 \
    # OpenGL / EGL
    libgl1 \
    libegl1 \
    libgles2 \
    # GLib
    libglib2.0-0 \
    # X11 base
    libx11-6 \
    libx11-xcb1 \
    libxext6 \
    libxrender1 \
    libdbus-1-3 \
    libfontconfig1 \
    # XCB platform plugin
    libxcb1 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    # Fonts
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
