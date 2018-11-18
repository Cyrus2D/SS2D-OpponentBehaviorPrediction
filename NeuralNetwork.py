import tensorflow as tf
import makedata as md

batch_size = 10
alpha = 0.00000001
n_epochs = 1000

datas = md.Data(batch_size)

x = tf.placeholder(tf.float32, [None, 48], "X")
y = tf.placeholder(tf.float32, [None, 2], "Y")

w1 = tf.Variable(tf.random_normal([48,100]), name="weight_1")
w2 = tf.Variable(tf.random_normal([100,50]), name="weight_2")
w3 = tf.Variable(tf.random_normal([50,2]), name="weight_out")

b1 = tf.Variable(tf.random_normal([1,100]), name="bias_1")
b2 = tf.Variable(tf.random_normal([1,50]), name="bias_2")
b3 = tf.Variable(tf.random_normal([1,2]), name="bias_out")

o1 = tf.nn.relu(tf.add(tf.matmul(x,w1), b1, name="o1"))
o2 = tf.nn.relu(tf.add(tf.matmul(o1,w2), b2, name="o2"))
o3 = (tf.add(tf.matmul(o2,w3), b3, name="o3"))

logits = o3
entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y, name="loss")
loss = tf.reduce_mean(entropy, name="loss2")

optimizer = tf.train.AdamOptimizer(alpha).minimize(loss)

diff = tf.subtract(logits, y)

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    n_batches = int(datas.n/batch_size)

    for epoch in range(n_epochs):
        epoch_loss = 0

        for batch in range(int(n_batches*9/10)):
            x_batch, y_batch = datas.get_batch()
            _, batch_loss = sess.run([optimizer, loss], feed_dict={x: x_batch, y: y_batch})
            epoch_loss += batch_loss
        datas.restart()
        print(epoch, epoch_loss/n_batches)

        if epoch%1 != 0:
            continue

        sum = [0, 0]
        for batch in range(int(n_batches/10)):
            x_batch, y_batch = datas.get_batch_t()
            di = sess.run([diff], feed_dict={x: x_batch, y: y_batch})
            for d in di[0]:
                sum[0] += d[0]
                sum[1] += d[1]
        sum[0] = sum[0]/n_batches*10
        sum[1] = sum[1]/n_batches*10
        print(sum)
