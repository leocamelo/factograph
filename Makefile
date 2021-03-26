default:
	aws s3 sync s3://pluga.co/apps/icons icons --exclude .gitkeep --delete
	python3 factograph.py
	aws s3 sync dist s3://pluga.co/automatizations-pages-social --exclude .gitkeep

install:
	pip3 install --upgrade pip
	pip3 install -r requirements.txt
