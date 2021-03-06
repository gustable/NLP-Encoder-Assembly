import unittest
import numpy as np
from numpy.linalg import norm
import tensorflow as tf

from numpy.random import seed

from nlp_enc import vae_old as vae
from nlp_enc.VAEAlexAdam import VAEAlexAdam
from . import random_init

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class TestVaeAlexAdam(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,  13, 717,
                465,   2,  10,  10,  13, 391,  24, 126,  31,   2,  12,  21,  17,
                230,  17, 146,   2,   4, 123, 144,  24,  28,  77,   2, 262,  18,
                160, 834, 123,   2,  56,  10,  10, 146, 886,   4,   2, 150,  36,
                26, 399,   6, 184,  52, 292,   7,   2,   2,  21,  13, 131, 104,
                75, 144,  79,   6, 248,  20,  42, 142,  10,  10,   4,   2,   2,
                456],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   2,   2, 215,
                28,  77,   2,  34,   6,   2, 373,   2,  88,  29,  43, 191, 387,
                140,   7,   4,   2,   4, 297, 799,   2,   2,   2,  12,  32,  18,
                25,  16,   2,  33, 222,  11, 363,  11,   2,   4, 172,   2,  17,
                2,   2,   2, 139, 133, 799,   2,  16,  35,   2,   6,   2,   6,
                2,   2,   7,   6,   2,   2,   2,   5, 545,   2,   2,   5,  17,
                256,  34,   2,   2,  59,  16, 642,  21,   4,  20,   2,  15,  75,
                193,  14,   2, 427, 615, 137,  17,   2,   2,   4, 172,   2,  11,
                4,   2,  12,  32, 139,   4, 107,   2,   2,   2,   5,  11,   4,
                236,   2, 234,   4,  20, 271, 125,   4,   2,   2,  83,   4,   2,
                5,   2,  50,  26,  57,   2,  12, 100,  28, 952,  48,   4,   2,
                7,   4, 139,  19,   4, 689,   2,   2,   5,  68,   2,  19, 799,
                2,  77,   2,   4, 172,  17,   4, 799,   2, 139,  42,  48,   4,
                799,   2, 139,  77,   2,  53,   2,  14,  96, 331, 152, 157,  33,
                32],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   1,  14,   9,   6,  20,  13,  69, 115,  60, 197,   7,
                319, 366,  61, 342, 291, 154,   2,  12,  33,   4, 374,   2,   5,
                2,  12, 103,   2,   4,   2, 431,   7,   4,   2,  23,   2,   2,
                75, 188,  12,   5,  28, 296,  12,   2, 237,  11, 192,   2,   2,
                12, 450, 211, 237,  50,  26,  55, 171, 701,   2, 102,  15,  61,
                492,  80, 106,   5, 990, 692,   8,  51,   6, 327, 653,  39,   2,
                5,   4, 117,   2,   4, 116,   9,   2,   4, 690,  26,   2,  36,
                79, 933,  83, 129, 419,   5,  25, 191, 339,  21,   2, 367,   4,
                769, 137,   2,  44,   2,   9,   2,  11,  45, 205,  96,   5,  50,
                9, 142, 162,   8,  67, 175,  58,  25, 106, 207, 557,  12,   2,
                8,   2,   2,  21,  13, 104,  36,  26, 107,  55, 275, 102, 199,
                321,  21, 820,  61, 492,  47,  57, 602,  33,  32,  11,   2,   2,
                14,   9,  31,   7, 148, 102,  15, 362,  80, 181,   8, 106, 120,
                5, 120, 174,   5,  31,  15, 846, 528, 330,   2,  19,  50,  26,
                504,  75, 106,  12, 159,   2,  58,   5,   2,  58,   5,  13,  92,
                235,  15,   2, 582,  15, 266,  54,  29, 494,   8,   2, 101,  85,
                20]])

        self.y = np.array([1, 0, 1])

        self.expected_shapes = [(1000, 64),
                    (64, 2000),
                    (500, 2000),
                    (2000,),
                    (64, 2000),
                    (500, 2000),
                    (2000,),
                    (1000, 2000),
                    (500, 2000),
                    (2000,),
                    (1000, 2000),
                    (500, 2000),
                    (2000,),
                    (1000, 435),
                    (435,),
                    (435, 200),
                    (200,),
                    (435, 200),
                    (200,),
                    (200, 2000),
                    (500, 2000),
                    (2000,),
                    (500, 2000),
                    (500, 2000),
                    (2000,),
                    (200, 100),
                    (100,),
                    (500, 1000),
                    (1000,),
                    (100, 1),
                    (1,)]


    def tearDown(self):
        pass

    def test_create_vae(self):
        MAX_LENGTH = 300
        NUM_WORDS = 1000
        h = vae.Hyper(vocab_size=NUM_WORDS, max_length=MAX_LENGTH)
        model = VAEAlexAdam(h)

        preds = model.autoencoder.predict(x=self.X)

        expected = (3, 300, 1000)
        self.assertEqual(expected, preds[0].shape)
        expected = (3, 1)
        self.assertEqual(expected, preds[1].shape)

        expected = self.expected_shapes
        actual = [w.shape for w in model.autoencoder.get_weights()]
        self.assertEqual(expected, actual)

        self.assertEqual(preds[0].shape, (3, 300, 1000))
        self.assertEqual(preds[1].shape, (3,1))
        
    def test_random_init(self):
        MAX_LENGTH = 300
        NUM_WORDS = 1000
        h = vae.Hyper(vocab_size=NUM_WORDS, max_length=MAX_LENGTH)

        expected = 0.023570226039551584
        actual = random_init.scale([100, 200])
        self.assertAlmostEqual(expected, actual)

        r0 = np.random.RandomState(42)
        expected = [random_init.scale(shape) * r0.uniform(size=shape) for shape in self.expected_shapes]

        model = VAEAlexAdam(h)
        r1 = np.random.RandomState(42)
        actual = random_init.random_w(r1, model.autoencoder)

        for u, v in zip(expected, actual):
            self.assertAlmostEqual(0, norm(u - v))

    def test_save_and_load_vae(self):
        MAX_LENGTH = 300
        NUM_WORDS = 1000
        h = vae.Hyper(vocab_size=NUM_WORDS, max_length=MAX_LENGTH)

        r0 = np.random.RandomState(42)
        expected = [random_init.scale(shape) * r0.uniform(size=shape) for shape in self.expected_shapes]

        model = VAEAlexAdam(h)
        model.autoencoder.set_weights(expected)

        model.autoencoder.save('data/autoencode.h5')
        
        model2 = VAEAlexAdam(h)
        model2.autoencoder.load_weights('data/autoencode.h5')

        actual = model2.autoencoder.get_weights()
        
        for u, v in zip(expected, actual):
            self.assertAlmostEqual(0, norm(u - v), 6)

    def test_model_evaluation(self):
        seed_value = 1234
        seed(seed_value)
           
        tf.set_random_seed(seed_value)
        session_conf = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
        sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)

        MAX_LENGTH = 300
        NUM_WORDS = 1000
        h = vae.Hyper(vocab_size=NUM_WORDS, max_length=MAX_LENGTH)

        temp = np.zeros((self.X.shape[0], MAX_LENGTH, NUM_WORDS))
        temp[np.expand_dims(np.arange(self.X.shape[0]), axis=0).reshape(self.X.shape[0], 1), np.repeat(np.array([np.arange(MAX_LENGTH)]), self.X.shape[0], axis=0), self.X] = 1
        self.X_one_hot = temp
      
        model = VAEAlexAdam(h)
        out = model.autoencoder.evaluate(x=self.X, y={'decoded_mean': self.X_one_hot, 'pred': self.y}, batch_size=10)
    
        expected = [3.0580520629882812,
                    2.3692352771759033,
                    0.6888167858123779,
                    0.0011111111380159855,
                    0.6666666865348816]
    
        self.assertEqual(expected, out)

    def test_model_prediction(self):
        seed_value = 1234
        seed(seed_value)

        tf.set_random_seed(seed_value)
        
        MAX_LENGTH = 300
        NUM_WORDS = 1000
        h = vae.Hyper(vocab_size=NUM_WORDS, max_length=MAX_LENGTH)

        temp = np.zeros((self.X.shape[0], MAX_LENGTH, NUM_WORDS))
        temp[np.expand_dims(np.arange(self.X.shape[0]), axis=0).reshape(self.X.shape[0], 1), np.repeat(np.array([np.arange(MAX_LENGTH)]), self.X.shape[0], axis=0), self.X] = 1
        self.X_one_hot = temp

        model = VAEAlexAdam(h)
        model.autoencoder.evaluate(x=self.X, y={'decoded_mean': self.X_one_hot, 'pred': self.y}, batch_size=1)
        pred = model.autoencoder.predict(self.X[0].reshape(1,-1))[1][0][0]
        expected = 0.4988190531730652
        self.assertEqual(np.float(pred), np.float(expected))
