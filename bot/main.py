from bot.router import app, machine

app.run(debug=True, port=5000, host='0.0.0.0')
# machine._bot.polling()
