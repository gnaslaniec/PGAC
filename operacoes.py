import psycopg2
import yaml

class Operacoes(object):

    # Conexão localhost
    def conexao_bd_local():
        con = psycopg2.connect(
            database="pgac",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        ) 
        cur = con.cursor()
        return con, cur
        
    def conexao_bd_rds(conf):
        con = psycopg2.connect(
            database=conf['db_rds']['database'],
            user=conf['db_rds']['user'],
            password=conf['db_rds']['password'],
            host=conf['db_rds']['host'],
            port=conf['db_rds']['port']
        )
        cur = con.cursor()
        return con, cur

    def retorna_saldo_usuario(cursor, id_usuario):
        cursor.execute("""select saldo from usuario where id = %s""", (id_usuario,))
        saldo = cursor.fetchone()
        return saldo[0]

    def atualiza_saldo(db,cursor,saldo,id_usuario):
        saldo_atualizado = saldo - 450
        cursor.execute("""update usuario set saldo = %s where id = %s""", (saldo_atualizado,id_usuario))
        db.commit()