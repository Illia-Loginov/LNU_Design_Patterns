const User = require('../models/User');

class Account {
    constructor(user) {
        if(!user) throw new Error('User not found');
        this.user = user;
    }

    getBalance() {
        return this.user.balance;
    }

    async withdraw(amount) {
        this.user.balance = (this.user.balance - Number(amount));
        await this.user.save();
    }
}

class AccountDatabase {
    static async login(account_id) {
        return new Account(await User.findById(account_id));
    }

    static async signup() {
        return new Account(await User.create({}));
    }
}

class AccountProxy {
    constructor(account) {
        this.user = account.user;
        this.account = account;
    }

    getBalance() {
        return this.account.getBalance().toFixed(2);
    }

    async withdraw(amount) {
        const newBalance = (this.user.balance - Number(amount));
        if(newBalance < 0) throw new Error('Not enough money for withdrawal');
        else await this.account.withdraw(amount);
    }
}

class DatabaseProxy {
    static async login(account_id) {
        if(account_id.length !== 24) throw new Error('Invalid Account ID (must be 24 characters long)');
        else return new AccountProxy(await AccountDatabase.login(account_id));
    }

    static async signup() {
        return new AccountProxy(await AccountDatabase.signup());
    }
}

class ATMController {
    static async balance_post(req, res) {
        const { account_id } = req.body;
    
        let user = undefined;
        try {
            const account = await DatabaseProxy.login(account_id);
            user = account.user;
            res.render('index', { user, balance: account.getBalance(), error: undefined });
        } catch (error) {
            console.log(error);
            if(!error.message) error.message = 'ERROR';
            res.render('index', { user, balance: undefined, error: error.message })
        }
    }

    static async login_post(req, res) {
        const { account_id } = req.body;
    
        try {
            const account = await DatabaseProxy.login(account_id);
            res.render('index', { user: account.user, balance: undefined, error: undefined });
        } catch (error) {
            console.log(error);
            if(!error.message) error.message = 'ERROR';
            res.render('index', { user: undefined, balance: undefined, error: error.message })
        }
    }

    static async signup_post(req, res) {
        try {
            const account = await DatabaseProxy.signup();
            res.render('index', { user: account.user, balance: undefined, error: undefined });
        } catch (error) {
            console.log(error);
            if(!error.message) error.message = 'ERROR';
            res.render('index', { user: undefined, balance: undefined, error: error.message })
        }
    }

    static async logout_get(req, res) {
        res.redirect('/');
    }

    static async withdrawal_post(req, res) {
        const { account_id, amount } = req.body;
    
        let user = undefined;
        try {
            const account = await DatabaseProxy.login(account_id);
            user = account.user;
            await account.withdraw(amount);
            res.render('index', { user, balance: account.getBalance(), error: undefined });
        } catch (error) {
            console.log(error);
            if(!error.message) error.message = 'ERROR';
            res.render('index', { user, balance: undefined, error: error.message })
        }
    }
}

module.exports = ATMController;