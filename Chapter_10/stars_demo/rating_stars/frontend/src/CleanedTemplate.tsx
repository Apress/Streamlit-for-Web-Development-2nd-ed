import {
   Streamlit,
   StreamlitComponentBase,
   withStreamlitConnection,
}  from 'streamlit-component-lib'
import React, { ReactNode } from 'react'
interface State {}
class MyComponent extends StreamlitComponentBase<State> {
  public state = {}
  public render = (): ReactNode => {
   return (
    <div></div>
   )
  }
}
export default withStreamlitConnection(MyComponent)
