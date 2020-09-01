class Operacoes(object):

    def retorna_saldo_usuario(cursor, id_usuario):
        cursor.execute("""select saldo from usuario where id = %s""", (id_usuario,))
        saldo = cursor.fetchone()
        return saldo[0]

    def atualiza_saldo(db,cursor,saldo,id_usuario):
        saldo_atualizado = saldo - 4.50
        cursor.execute("""update usuario set saldo = %s where id = %s""", (saldo_atualizado,id_usuario))
        db.commit()