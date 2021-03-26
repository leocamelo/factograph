default:
	aws s3 sync s3://pluga.co/apps/icons icons --exclude .gitkeep --delete
	python factograph.py
	aws s3 sync dist s3://pluga.co/automatizations-pages-social --exclude .gitkeep

install:
	pip install --upgrade pip
	pip install -r requirements.txt
