const atmController = require('../controllers/atmController');

const router = require('express').Router();

router.post('/balance', atmController.balance_post);
router.post('/login', atmController.login_post);
router.post('/signup', atmController.signup_post);
router.get('/logout', atmController.logout_get);
router.post('/withdrawal', atmController.withdrawal_post);

module.exports = router;