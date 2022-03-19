build:
	curl https://pyenv.run | bash 
	ecoh 'export PATH="$HOME/.pyenv/bin:$PATH"' > ~/.bashrc
	ecoh 'eval "$(pyenv init --path)"' > ~/.bashrc
	ecoh 'eval "$(pyenv virtualenv-init -)"' > ~/.bashrc
	pyenv install 3.9.7
	pyenv local 3.9.7
	pip install -r requirements.txt

lexer:
	python analysers/lexical_analyser.py $(file)
	
compile:
	python compiler.py $(file)