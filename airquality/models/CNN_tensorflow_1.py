import tensorflow as tf


# Training Parameters
ETA = 0.001
LENGTH = 183
COLUMNS = 13

# Network Parameters
dropout = 0.6  # Dropout, probability to keep units


def conv_network(x_dict, dropout, reuse, is_training):
    with tf.variable_scope('conv_network', reuse=reuse):
        x = tf.cast(x_dict['data'], dtype=tf.float32)
        x = tf.reshape(x, shape=[-1, LENGTH, COLUMNS, 1])
        c1 = tf.layers.conv2d(x, 8, [7, 3], activation=tf.nn.relu)
        c1 = tf.layers.max_pooling2d(c1, [4, 2], 1)
        c2 = tf.layers.conv2d(x, 4, [14, 5], 7, activation=tf.nn.relu)
        c2 = tf.layers.max_pooling2d(c2, [3, 2], 1)
        d1 = tf.contrib.layers.flatten(c2)
        d1 = tf.layers.dense(d1, 128)
        d1 = tf.layers.dropout(d1, rate=dropout, training=is_training)
        o = tf.layers.dense(d1, 1)
        return tf.nn.sigmoid(o)


def model_fn(features, labels, mode):
    logits_train = conv_network(features, dropout, reuse=False,
                                is_training=True)
    logits_test = conv_network(features, dropout, reuse=True,
                               is_training=False)

    # Predictions
    pred_classes = tf.round(logits_test)

    # If prediction mode, early return
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode, predictions=pred_classes)

        # Define loss and optimizer
    loss_op = tf.losses.log_loss(labels=tf.cast(labels, dtype=tf.float32),
                                 predictions=logits_train)
    optimizer = tf.train.AdamOptimizer(learning_rate=ETA)
    train_op = optimizer.minimize(loss_op,
                                  global_step=tf.train.get_global_step())

    # TF Estimators requires to return a EstimatorSpec, that specify
    # the different ops for training, evaluating, ..accuracy.
    estim_specs = tf.estimator.EstimatorSpec(
        mode=mode,
        predictions=pred_classes,
        loss=loss_op,
        train_op=train_op,
        eval_metric_ops={
            'accuracy': tf.metrics.accuracy(labels=labels,
                                            predictions=pred_classes),
            'recall': tf.metrics.recall(labels=labels,
                                        predictions=pred_classes)
        })

    return estim_specs


def get_cnn(model_dir=None):
    if model_dir is not None:
        return tf.estimator.Estimator(model_fn=model_fn,
                                      model_dir=model_dir)
    else:
        return tf.estimator.Estimator(model_fn)
