const express = require('express');
const mongoose = require('mongoose');

const { body, validationResult } = require('express-validator/check');

const router = express.Router();

const persons = mongoose.model('persons');
mongoose.connect('localhost:27017/persons');
var Schema = mongoose.Schema;

router.get('/', (req, res) => {
    res.render('form', { title: 'Person form' });
  });

router.post('/', 
    (req, res) => {
    console.log(req.body);
    res.render('form', { title: 'Person form' });
     {
        const errors = validationResult(req);
        
        if (errors.isEmpty()) {
            console.log("no errorrxs")
            const person = new persons(req.body);
            person.save()
              .then(() => { res.send('Thank you for your registration!'); })
              .catch(() => { res.send('Sorry! Something went wrong.'); });          
            } 
           else {
            res.render('form', {
              title: 'Registration form',
              errors: errors.array(),
              data: req.body,
            });
          }
        }


router.post('/Averge', function (req, res) {
          console.log(req.body.todo + " is added to top of the list.");
          res.redirect('/');
        });

    
});


module.exports = router;