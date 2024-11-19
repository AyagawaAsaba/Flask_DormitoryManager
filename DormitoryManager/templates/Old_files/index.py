
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.cursor()
        cur.execute("SELECT * FROM pythonflask.users WHERE email=%s AND password=%s", (email, password))
        # cur.execute("SELECT * FROM pythonflask.users WHERE name=%s AND password=%s", (name, password))
        user = cur.fetchone()
        print(user)
        if user:
            session['user'] = user
            return redirect(url_for('dashboard'))

        else:
            flash('邮箱或密码错误')
    return render_template(
        'login.html',
        title="注册 | 学生注册管理",
        year=datetime.now().year,
        message='Your application Login Page.'
    )
    # return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.cursor()
        # 2、提交SQL语句
        sql = "INSERT INTO pythonflask.users(name, email, password) VALUES (%s, %s,%s)"
        cur.execute(sql, [name, email, password])
        # cur.execute("INSERT INTO pythonflask.users(name, email, password) VALUES(%s, %s, %s)", (name, email,
        # password))
        # cur.execute("INSERT INTO pythonflask.users(email, password) VALUES(%s, %s)", (email, password))
        mysql.commit()
        mysql.close()
        cur.close()
        flash('注册成功')
        return redirect(url_for('login'))

    return render_template(
        'register.html',
        title="注册 | 后台管理系统",
        year=datetime.now().year,
        message='Your application Register Page.'
    )
    # return render_template('index.html')
