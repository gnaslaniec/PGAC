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
            port=conf['db_rds']['port'],
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )
        cur = con.cursor()
        return con, cur

    def retorna_saldo_usuario(cursor, id_usuario):
        cursor.execute("""select saldo_centavos from usuario where id = %s""", (id_usuario,))
        saldo = cursor.fetchone()
        return saldo[0]

    def retorna_saldo_usuario_reais(cursor, id_usuario):
        cursor.execute("""select round(saldo,2) from usuario where id = %s""", (id_usuario,))
        saldo = cursor.fetchone()
        return saldo[0]

    def atualiza_saldo(db,cursor,saldo,id_usuario):
        saldo_atualizado_centavos = saldo - 450
        saldo_atualizado_reais = float(saldo_atualizado_centavos) / 100
        cursor.execute("""update usuario set saldo_centavos = %s where id = %s""", (saldo_atualizado_centavos,id_usuario))
        cursor.execute("""update usuario set saldo = %s where id = %s""", (saldo_atualizado_reais,id_usuario))
        db.commit()