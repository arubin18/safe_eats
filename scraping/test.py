test = "''''abc'"

def clean_string(var):
		''' remove innner quotes, semi-colons, and add quotes around var '''

		var = var.replace("'","")
		var = var.replace("\"","")
		var = var.replace(";","")
		var = var.replace(".","")
		var = var.replace(",","")
		var = "'" + var + "'"
		
		return var

print(clean_string(test))