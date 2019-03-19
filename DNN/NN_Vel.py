import tensorflow as tf
from DNN import makedata_vel as md
import matplotlib.pyplot as pt


def calc_diff(o, y):
    sum = [0, 0]
    for i in range(len(o)):
        sum[0] += abs(o[i][0] - y[i][0])
        sum[1] += abs(o[i][1] - y[i][1])
    return sum


batch_size = 128
alpha = 0.1
n_epochs = 100
changed_e = 0.0  # 0.35
drop = 1

datas = md.Data(batch_size)

nx = 94
ny = 2
x = tf.placeholder(tf.float32, [None, nx], "X")
y = tf.placeholder(tf.float32, [None, ny], "Y")
dropout = tf.placeholder(tf.float32)

n1 = 256
n2 = 64
# n3 = 32
n4 = ny

w1 = tf.Variable(tf.random_normal([nx, n1]), name="weight_1")
w2 = tf.Variable(tf.random_normal([n1, n2]), name="weight_2")
# w3 = tf.Variable(tf.random_normal([n2,n3]), name="weight_3")
w4 = tf.Variable(tf.random_normal([n2, n4]), name="weight_out")

b1 = tf.Variable(tf.random_normal([1, n1]), name="bias_1")
b2 = tf.Variable(tf.random_normal([1, n2]), name="bias_2")
# b3 = tf.Variable(tf.random_normal([1,n3]), name="bias_3")
b4 = tf.Variable(tf.random_normal([1, n4]), name="bias_out")

o1 = tf.nn.relu(tf.add(tf.matmul(x, w1), b1, name="o1"))
# o1 = tf.nn.dropout(o1, dropout)
o2 = tf.nn.relu(tf.add(tf.matmul(o1, w2), b2, name="o2"))
# o2 = tf.nn.dropout(o2, dropout)
# o3 = tf.nn.relu(tf.add(tf.matmul(o2,w3), b3, name="o3"))
o4 = (tf.add(tf.matmul(o2, w4), b4, name="o4"))

logits = o4
# entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y, name="loss")
delta = tf.square(tf.subtract(logits, y))
loss = tf.reduce_mean(delta, name="loss2")

optimizer = tf.train.AdamOptimizer(alpha).minimize(loss)

preds = tf.nn.softmax(logits)
coorrect_preds = tf.equal(tf.argmax(preds, 1), tf.argmax(y, 1))
accuracy = tf.reduce_sum(tf.cast(coorrect_preds, tf.float32))

saver = tf.train.Saver()

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    dots = [[], []]

    for epoch in range(n_epochs):
        epoch_loss = 0
        learn_preds = 0

        n_batches = int(len(datas.x) / batch_size)
        for batch in range(n_batches):
            x_batch, y_batch = datas.get_batch()
            _, batch_loss = sess.run([optimizer, loss], feed_dict={x: x_batch, y: y_batch, dropout: drop})
            epoch_loss += batch_loss
        dots[1].append(learn_preds / len(datas.x))
        datas.restart()
        print(epoch, epoch_loss / n_batches)
        if epoch_loss / n_batches < changed_e:
            alpha /= 10
            changed_e /= 2

        if epoch % 1 != 0:
            continue

        diffs = [0, 0]
        n_batches = int(len(datas.x_t) / batch_size)
        for batch in range(n_batches):
            x_batch, y_batch = datas.get_batch_t()
            o = sess.run(o4, feed_dict={x: x_batch, y: y_batch, dropout: 1})
            # print(o)
            # print(y)
            # input()
            diff = calc_diff(o, y_batch)
            # print(diff)
            # input()
            diffs[0] += diff[0]
            diffs[1] += diff[1]
            # print("t", accuracy_batch)
        # print(diffs[0] / len(datas.x_t))
        # print(diffs[1] / len(datas.x_t))
        dots[0].append(diffs[0] / len(datas.x_t))
        dots[1].append(diffs[1] / len(datas.x_t))
        # print("ACC",total_correct_preds/len(datas.x_t))

        if epoch % 50 == 49:
            pt.plot(dots[1], "r")
            pt.plot(dots[0], "b")
            pt.ylabel("alpha: " + str(alpha))
            pt.xlabel("last_ACC: " + str(diffs[0] / len(datas.x_t)))
            pt.show()

        saver.save(sess, "./DNN/logs/SaveforLoadVel2/SLV.ckpt")

file = open("VelFT.dots", "w")
for i in range(len(dots[0])):
    line = str(dots[0][i]) + " " + str(dots[0][1])
    file.write(line + "\n")
