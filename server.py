import argparse
import os
import logging
from flask import Flask, request, jsonify, send_from_directory

# === Configuration ===

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simple Flask file server")
    parser.add_argument("--upload-dir", type=str, default="/srv/cdn/uploads", help="Directory to save uploaded files")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()

def configure_logger(debug_enabled):
    level = logging.DEBUG if debug_enabled else logging.INFO
    logging.basicConfig(level=level)
    return logging.getLogger(__name__)

# === Flask App ===

def create_app(upload_dir, logger):
    app = Flask(__name__)

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        logger.info(f"Created upload directory at {upload_dir}")

    @app.route("/upload", methods=["POST"])
    def upload_file():
        """
        Endpoint to handle file uploads via POST.
        """
        if "file" not in request.files:
            logger.warning("No file part in request")
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]

        if file.filename == "":
            logger.warning("No selected file")
            return jsonify({"error": "No selected file"}), 400

        filepath = os.path.join(upload_dir, file.filename)
        file.seek(0)
        file.save(filepath)

        logger.info(f"File uploaded: {file.filename}")
        return jsonify({"filename": file.filename}), 200

    @app.route("/download/<filename>", methods=["GET"])
    def download_file(filename):
        """
        Endpoint to download a file if it exists.
        """
        try:
            file_path = os.path.join(upload_dir, filename)
            if os.path.exists(file_path):
                return send_from_directory(upload_dir, filename, as_attachment=True)
            else:
                logger.warning(f"File not found: {filename}")
                return jsonify({"error": "File not found"}), 404
        except Exception as e:
            logger.error(f"Error during download: {e}")
            return jsonify({"error": str(e)}), 500

    return app

# === Entry Point ===

if __name__ == "__main__":
    args = parse_arguments()
    logger = configure_logger(args.debug)
    app = create_app(args.upload_dir, logger)
    app.run(host=args.host, port=args.port, debug=args.debug)
