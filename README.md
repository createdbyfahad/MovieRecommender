# Movie Recommender 

## Author:

Fahad Alarefi


### Prerequisites:  

Required to install and run the software:

 * [python3](https://www.python.org/)
 * [python3-venv](https://docs.python.org/3/tutorial/venv.html)

#### Installing Prerequisites:  

##### MACOS:  

You need to install [homebrew](https://brew.sh/) first. If you already have homebrew 
on your machine, you can skip step 1.  

```
1. /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)".  
2. brew install python3
3. pip3 install virtualenv 
```
		
##### Ubuntu:
```  
1. sudo apt-get install python3
2. sudo apt-get install python3-venv  
```
##### Fedora: 
``` 
sudo yum install python36  
```

 Python3.4+ include the venv module on Fedora.  

### How to train model:
The dataset is located api/models/100k/ratings.csv
Update necesserary variables in train.py
and execute train.py
Update the trained model file_location in flask_main.py

### How to Run Server:

	1. virtualenv venv
	2. source venv/bin/activate
	3. pip install -r requirements.txt
	4. python flask_main.py
	5. Ctrl+C to quit  
