default:
	python3 -m awscli s3 sync s3://pluga.co/apps/icons icons --exclude .gitkeep --delete
	python3 factograph.py
	python3 -m awscli s3 sync dist/social s3://pluga.co/automatizations-pages-social --exclude .gitkeep --size-only
	python3 -m awscli s3 sync dist/email s3://pluga.co/emails/notifications/tools --exclude .gitkeep --size-only

install:
	pip3 install --user --upgrade pip
	pip3 install --user -r requirements.txt
