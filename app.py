from flask import Flask

from core.elasticsearch.es import close_es, update_es_command, create_index_command

app = Flask(__name__)
app.teardown_appcontext(close_es)
app.cli.add_command(update_es_command)
app.cli.add_command(create_index_command)

# noinspection PyUnresolvedReferences
import views.likes


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)