def load_css():
    return """
    <style>
        .card {
            background: rgba(255, 255, 255, 0.06);
            padding: 20px;
            border-radius: 14px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
        }

        .title {
            font-size: 22px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        }

        .score {
            font-size: 36px;
            font-weight: bold;
            color: #facc15;
        }

        ul {
            padding-left: 20px;
        }

        li {
            margin-bottom: 6px;
            color: #e5e7eb;
        }

        p {
            color: #d1d5db;
            line-height: 1.6;
        }
    </style>
    """