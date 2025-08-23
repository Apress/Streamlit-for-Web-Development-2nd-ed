import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from datetime import datetime
from Utils import *
# Plotly confusion matrix visualization
def confusion_matrix_plot(y_test, y_pred):
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    z = cnf_matrix.tolist()[::-1]
    x = ['Negative', 'Positive']
    y = ['Positive', 'Negative']
    z_text = z
    fig = ff.create_annotated_heatmap(z, x, y, annotation_text=z_text, text=z,
    hoverinfo='text', colorscale='Blackbody')
    st.write(fig)
# Plotly receiver operating characteristic visualization function
def roc_plot(X_test, logreg, y_test):
    y_pred_proba = logreg.predict_proba(X_test)[::,1]
    fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)
    roc_data = pd.DataFrame([])
    roc_data['True positive'] = tpr
    roc_data['False positive'] = fpr
    fig = px.line(roc_data, x='False positive', y='True positive')
    st.write(fig)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    st.info(f'Area Under Curve: **{ round(auc,3)}**')
# Hyperparameters expander function
def lr_hyperparameters():
    with st.expander('Advanced Parameters'):
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            penalty = st.selectbox('Penalty', ['l2','l1','elasticnet','none'])
            tol = st.number_input('Tolerance (1e-4)', value=1)/10000
            fit_intercept = st.radio('Intercept', [True,False])
            class_weight = st.radio('Class weight', [None,'balanced'])
            solver = st.selectbox('Solver', ['lbfgs','newton-cg','liblinear','sag',
            'saga'])
            multi_class = st.selectbox('Multi class', ['auto','ovr','multinomial'])
            warm_start = st.radio('Warm start', [False,True])
        with col2_2:
            dual = st.radio('Dual or primal formulation', [False,True])
            C = st.number_input('Inverse regularization strength', 0.0, 99.0, 1.0, 0.1)
            intercept_scaling = st.number_input('Intercept scaling', 0.0, 99.0, 1.0, 0.1)
            random_state = st.radio('Random state', [None,'Custom'])
            if random_state == 'Custom':
                random_state = st.number_input('Custom random state', 0, 99, 1, 1)
            max_iter = st.number_input('Maximum iterations', 0, 100, 100, 1)
            verbose = st.number_input('Verbose', 0, 99, 0, 1)
            l1_ratio = st.radio('L1 ratio', [None,'Custom'])
            if l1_ratio == 'Custom':
                l1_ratio = st.number_input('Custom l1 ratio', 0.0, 1.0, 1.0, 0.01)
        #Download hyperparameters feature
        hyperparameters = {'penalty':[penalty], 'dual':[dual], 'tol':[tol], 'C':[C],
        'fit_intercept':[fit_intercept], 'intercept_scaling':[intercept_scaling],
        'class_weight':[class_weight],
        'random_state':[random_state],
        'solver':[solver], 'max_iter':[max_iter], 'multi_class':[multi_class],
        'verbose':[verbose],'warm_start':[warm_start], 'l1_ratio':[l1_ratio]}
        st.download_button(
            label='Download hyperparameters',
            data=pd.DataFrame(hyperparameters).to_csv(index=False).encode('utf-8'),
            file_name='Hyperparameters.csv',
        )
    return (penalty, tol, fit_intercept, class_weight, solver, multi_class, warm_start, dual, C, intercept_scaling,
    random_state, max_iter, verbose, l1_ratio)
# Logistic regression training function
@st.cache_resource
def log_train(df, feature_cols, label_col, test_size, penalty, tol, fit_intercept, class_weight, solver, multi_class,
    warm_start, dual, C, intercept_scaling, random_state,
    max_iter, verbose, l1_ratio):
    x = df[feature_cols]
    y = df[label_col]
    x_train,x_test,y_train,y_test=train_test_split(x, y, test_size=test_size, random_state=0)
    logreg = LogisticRegression(penalty=penalty, dual=dual, tol=tol, C=C, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, class_weight=class_weight,
    random_state=random_state, solver=solver, max_iter=max_iter,
    multi_class=multi_class, verbose=verbose, warm_start=
    warm_start, l1_ratio=l1_ratio)
    logreg.fit(x_train,y_train)
    y_pred = logreg.predict(x_test)
    return x_train, x_test, y_train, y_test, y_pred, logreg
# Logisitic regression predictor function
def log_real(logreg, df_real, feature_cols, label_col):
    x_test_real = df_real[feature_cols]
    y_pred_real = logreg.predict(x_test_real)
    x_pred_real = df_real.copy()
    x_pred_real[label_col] = y_pred_real
    return x_pred_real.sort_index()
# Prediction statistics function
def stats(y_test, y_pred):
    accuracy = metrics.accuracy_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred)
    f1 = metrics.f1_score(y_test, y_pred)
    col2_1, col2_2, col2_3, col2_4 = st.columns(4)
    with col2_1:
        st.info(f'Accuracy: **{round(accuracy,3)}**')
    with col2_2:
        st.info(f'Precision: **{round(precision,3)}**')
    with col2_3:
        st.info(f'Recall: **{round(recall,3)}**')
    with col2_4:
        st.info(f'F1 Score: **{round(f1,3)}**')
def lr_main(engine):
    _, session_id = get_session()
    insert_row(session_id, engine)
    update_row('lr1',datetime.now().strftime('%H:%M:%S %d/%m/%Y'), session_id, engine)
    if st.session_state['df_train'] is not None:
        df = st.session_state['df_train']
        update_row('data1_rows',len(df),session_id,engine)
        update_row('lr2',datetime.now().strftime('%H:%M:%S %d/%m/%Y'), session_id,
         engine)
        st.title('Training')
        st.subheader('Parameters')
        col1, col2, col3 = st.columns((3,3,2))
        with col1:
            feature_cols = st.multiselect('Please select features', df.columns)
        with col2:
            label_col = st.selectbox('Please select label', df.columns)
        with col3:
            test_size = st.number_input('Please enter test size', 0.01, 0.99, 0.25, 0.05)
        (penalty, tol, fit_intercept, class_weight, solver, multi_class,
        warm_start, dual, C, intercept_scaling, random_state, max_iter, verbose,
        l1_ratio) = lr_hyperparameters()
        try:
            x_train, x_test, y_train, y_test, y_pred, logreg = log_train(df, feature_cols, label_col, test_size,
            penalty, tol, fit_intercept, class_weight, solver,
            multi_class, warm_start, dual, C, intercept_scaling,
            random_state, max_iter, verbose, l1_ratio)
            st.subheader('Confusion Matrix')
            confusion_matrix_plot(y_test, y_pred)
            st.subheader('Metrics')
            stats(y_test, y_pred)
            st.subheader('ROC Curve')
            roc_plot(x_test, logreg, y_test)
            update_row('lr3',datetime.now().strftime('%H:%M:%S %d/%m/%Y'),
            session_id, engine)
            if st.session_state['df_real'] is not None:
                try:
                    df_real = st.session_state['df_real']
                    st.title('Testing')
                    update_row('data2_rows',len(df_real), session_id, engine)
                    st.subheader('Predicted Labels')
                    x_pred_real = log_real(logreg, df_real, feature_cols, label_col)
                    st.write(x_pred_real)
                    update_row('lr4',datetime.now().strftime('%H:%M:%S %d/%m/%Y'),
                    session_id, engine)
                    st.download_button(
                         label='Download predicted labels',
                         data=pd.DataFrame(x_pred_real).to_csv(index=False)
                         .encode('utf-8'),
                         file_name='Predicted labels.csv',
                    )
                except:
                    st.warning('Please upload a test dataset with the same feature set as the training dataset')
            elif st.session_state['df_real'] is None:
                st.sidebar.warning('Please upload a test dataset')
        except:
            st.warning('Please select at least one feature, a suitable binary label and appropriate advanced parameters')
    elif st.session_state['df_train'] is None:
        st.title('Welcome     ')
        st.subheader('Please use the left pane to upload your dataset')
        st.sidebar.warning('Please upload a training dataset')
