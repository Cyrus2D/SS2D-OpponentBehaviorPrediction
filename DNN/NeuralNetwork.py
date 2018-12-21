import tensorflow as tf
from DNN import makedata as md
import matplotlib.pyplot as pt

batch_size = 128
alpha = 0.00000001
n_epochs = 10000
changed_e = 0

datas = md.Data(batch_size)

nx = 48
x = tf.placeholder(tf.float32, [None, nx], "X")
y = tf.placeholder(tf.float32, [None, 2], "Y")

n1 = 512
n2 = 128
# n3 = 32
n4 = 2

w1 = tf.Variable(tf.random_normal([nx,n1]), name="weight_1")
w2 = tf.Variable(tf.random_normal([n1,n2]), name="weight_2")
# w3 = tf.Variable(tf.random_normal([n2,n3]), name="weight_3")
w4 = tf.Variable(tf.random_normal([n2,n4]), name="weight_out")

b1 = tf.Variable(tf.random_normal([1,n1]), name="bias_1")
b2 = tf.Variable(tf.random_normal([1,n2]), name="bias_2")
# b3 = tf.Variable(tf.random_normal([1,n3]), name="bias_3")
b4 = tf.Variable(tf.random_normal([1,n4]), name="bias_out")

o1 = tf.nn.relu(tf.add(tf.matmul(x,w1), b1, name="o1"))
o2 = tf.nn.relu(tf.add(tf.matmul(o1,w2), b2, name="o2"))
# o3 = tf.nn.relu(tf.add(tf.matmul(o2,w3), b3, name="o3"))
o4 = (tf.add(tf.matmul(o2 ,w4), b4, name="o4"))

logits = o4
entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y, name="loss")
loss = tf.reduce_mean(entropy, name="loss2")

optimizer = tf.train.AdamOptimizer(alpha).minimize(loss)

preds = tf.nn.softmax(logits)
coorrect_preds = tf.equal(tf.argmax(preds,1), tf.argmax(y,1))
accuracy = tf.reduce_sum(tf.cast(coorrect_preds, tf.float32))
diff = tf.subtract(o4, y)
sum_diff = tf.reduce_sum(diff, axis=0)

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    n_batches = int(len(datas.x)/batch_size)
    dots = [[],[]]

    for epoch in range(n_epochs):
        epoch_loss = 0

        for batch in range(n_batches):
            x_batch, y_batch = datas.get_batch()
            _, batch_loss = sess.run([optimizer, loss], feed_dict={x: x_batch, y: y_batch})
            epoch_loss += batch_loss
        datas.restart()
        print(epoch, epoch_loss/n_batches)
        dots[1].append(epoch_loss/n_batches)
        if epoch_loss/n_batches < changed_e:
            alpha /= 10
            changed_e /= 2

        if epoch%1 != 0:
            continue

        n_batches = int(len(datas.x_t)/batch_size)
        sum = 0
        for batch in range(n_batches):
            x_batch, y_batch = datas.get_batch_t()
            s = sess.run(sum_diff, feed_dict={x: x_batch, y: y_batch})
            sum += s
        dots[0].append(sum/len(datas.x_t))
        # print("ACC",total_correct_preds/len(datas.x_t))

        if epoch%100 == 99:
            # pt.plot(dots[1], "r")
            pt.plot(dots[0], "b")
            pt.ylabel("alpha: " +str(alpha))
            pt.xlabel("last_ACC: " +str(sum/len(datas.x_t)))
            pt.show()
