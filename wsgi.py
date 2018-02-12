from bow import app

if __name__ == "__main__":
	app.secret_key = b'\n\x1e\xcc\xa3\xdf2g*\x8c,YX\x95v[\xb1\xa7\xdcLu\x0f\xfcT@'
	app.run(debug=False)
