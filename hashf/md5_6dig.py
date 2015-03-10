import md5

def evaluteHash (text):
	return md5.new(text).hexdigest()[0:6]
