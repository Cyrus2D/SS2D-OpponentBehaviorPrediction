import tensorflow as tf
from DNN import makedata as md
import matplotlib.pyplot as pt

batch_size = 128
alpha = 0.001
n_epochs = 200
changed_e = 0 # 0.35
drop = 1

datas = md.Data(batch_size)

nx = 94
x = tf.placeholder(tf.float32, [None, nx], "X")
y = tf.placeholder(tf.float32, [None, 11], "Y")
dropout = tf.placeholder(tf.float32)

n1 = 256
n2 = 64
# n3 = 32
n4 = 11

# w3 = tf.Variable(tf.random_normal([n2,n3]), name="weight_3")

# b3 = tf.Variable(tf.random_normal([1,n3]), name="bias_3")

# o1 = tf.nn.dropout(o1, dropout)
# o2 = tf.nn.dropout(o2, dropout)
# o3 = tf.nn.relu(tf.add(tf.matmul(o2,w3), b3, name="o3"))


with tf.variable_scope("Layer1"):
    w1 = tf.Variable(tf.random_normal([nx,n1]), name="weight_1")
    b1 = tf.Variable(tf.random_normal([1, n1]), name="bias_1")
    o1 = tf.nn.relu(tf.add(tf.matmul(x, w1), b1, name="o1"))

with tf.variable_scope("Layer2"):
    w2 = tf.Variable(tf.random_normal([n1, n2]), name="weight_2")
    b2 = tf.Variable(tf.random_normal([1, n2]), name="bias_2")
    o2 = tf.nn.relu(tf.add(tf.matmul(o1, w2), b2, name="o2"))

with tf.variable_scope("Out"):
    w4 = tf.Variable(tf.random_normal([n2, n4]), name="weight_out")
    b4 = tf.Variable(tf.random_normal([1, n4]), name="bias_out")
    o4 = (tf.add(tf.matmul(o2, w4), b4, name="o4"))


logits = o4
entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y, name="loss")
loss = tf.reduce_mean(entropy, name="loss2")

optimizer = tf.train.AdamOptimizer(alpha).minimize(loss)

preds = tf.nn.softmax(logits)
coorrect_preds = tf.equal(tf.argmax(preds,1), tf.argmax(y,1))
accuracy = tf.reduce_sum(tf.cast(coorrect_preds, tf.float32))

writer = tf.summary.FileWriter('./DNN/graphs', tf.get_default_graph())
writer.close()

saver = tf.train.Saver()

init = tf.global_variables_initializer()
with tf.Session() as sess:
    # sess.run(init)
    saver.restore(sess, './DNN/logs/SM.ckpt')
    dots = [[], []]

    for epoch in range(n_epochs):
        epoch_loss = 0
        learn_preds = 0

        n_batches = int(len(datas.x) / batch_size)
        for batch in range(n_batches):
            x_batch, y_batch = datas.get_batch()
            _, batch_loss, acc = sess.run([optimizer, loss, accuracy], feed_dict={x: x_batch, y: y_batch, dropout: drop})
            learn_preds += acc
            # print(acc)
            epoch_loss += batch_loss
        dots[1].append(learn_preds / len(datas.x))
        datas.restart()
        print(epoch, epoch_loss/n_batches)
        if epoch_loss/n_batches < changed_e:
            alpha /= 10
            changed_e /= 2

        if epoch%1 != 0:
            continue

        total_correct_preds = 0
        n_batches = int(len(datas.x_t)/batch_size)
        for batch in range(n_batches):
            x_batch, y_batch = datas.get_batch_t()
            accuracy_batch = sess.run(accuracy, feed_dict={x: x_batch, y: y_batch, dropout: 1})
            # print("t", accuracy_batch)
            total_correct_preds += accuracy_batch
        dots[0].append(total_correct_preds/len(datas.x_t))
        # print("ACC",total_correct_preds/len(datas.x_t))

        if epoch%100 == 99:
            pt.plot(dots[1], "r")
            pt.plot(dots[0], "b")
            pt.ylabel("alpha: " +str(alpha))
            pt.xlabel("last_ACC: " +str(total_correct_preds/len(datas.x_t)))
            pt.show()

    saver.save(sess, "./DNN/logs/SM.ckpt")